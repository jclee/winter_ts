import ika
from browser import window

import saveloadmenu

from player import Player, PLAYER_SPRITE
from anklebiter import AnkleBiter
from carnivore import Carnivore
from devourer import Devourer
from razormane import RazorMane
from dragonpup import DragonPup
from hellhound import HellHound
from yeti import Yeti
from gorilla import Gorilla
from soulreaver import SoulReaver
from dynamite import Dynamite
from savepoint import SavePoint
from obstacle import IceWall, Gap, IceChunks, Boulder
from rune import WaterRune, FireRune, WindRune, CowardRune, StrengthRune, PowerRune, GuardRune

from hud import HPBar, MPBar, EXPBar
from caption import Caption
from camera import Camera
from gameover import GameLoseException, GameQuitException, GameWinException

import subscreen

import controls
import cabin
import ending
import sound

FRAME_RATE = 100
MAX_SKIP_COUNT = 10
START_MAP = 'map01.ika-map'
START_POS = (34 * 16, 23  * 16)

spawnMap = {
    # match each sprite name up with the associated class
    'anklebiter.ika-sprite': AnkleBiter,
    'carnivore.ika-sprite': Carnivore,
    'devourer.ika-sprite': Devourer,
    'razormane.ika-sprite': RazorMane,
    'dragonpup.ika-sprite': DragonPup,
    'hellhound.ika-sprite': HellHound,
    'yeti.ika-sprite': Yeti,
    'gorilla.ika-sprite': Gorilla,
    'soulreaver.ika-sprite': SoulReaver,

    'dynamite.ika-sprite': Dynamite,
    'waterrune.ika-sprite': WaterRune,
    'firerune.ika-sprite': FireRune,
    'windrune.ika-sprite': WindRune,
    'cowardrune.ika-sprite': CowardRune,
    'strengthrune.ika-sprite': StrengthRune,
    'powerrune.ika-sprite': PowerRune,
    'guardrune.ika-sprite': GuardRune,

    'savepoint.ika-sprite': SavePoint,

    'icecave.ika-sprite': IceWall,
    'ice.ika-sprite': IceWall,
    'icechunks.ika-sprite': IceChunks,
    'boulder.ika-sprite': Boulder,
    'vgap.ika-sprite': Gap,
    'hgap.ika-sprite': Gap,
}

class Engine(object):
    '''Core engine thingie.  bleh.'''

    dir = window.Dir

    def __init__(self):
        self.entities = []
        self.killList = []
        self.things = []
        self.mapThings = [] # same as self.things, but is cleared every mapSwitch
        self.fields = []

        # ika Entity : Entity
        self.entFromEnt = {}

        self.player = None
        self.background = None

        # framerate regulating stuff:
        self.ticksPerFrame = 100.0 / FRAME_RATE
        self.nextFrameTime = 0

        self._engine = ika.getEngine()
        self.map = self._engine.map
        self.font = window.FontClass.new(self._engine, 'system.fnt')
        self.mapName = ''

        self.fader = sound.Crossfader()
        # all music.  Never ever let go. (because I'm lazy)
        self.music = {
            'music/silence': sound.NullSound(),
        }
        self.saveFlags = {}

        def getEngine():
            return self._engine
        self.getEngine = getEngine

    def initTask(self, saveData = None):
        'barf'

        # clean everything
        self.killList = self.entities[:]
        self.clearKillQueue()
        self.things = []
        self.mapThings = []
        self.fields = []

        # ika Entity : Entity
        self.entFromEnt = {}

        # TODO - redundant with map switches in beginNewGameTask/loadGameTask? (pos parameter differs...)
        if saveData:
            # evil
            yield from self.mapSwitchTask(saveData.mapName, None, fade=False)
        else:
            yield from self.mapSwitchTask(START_MAP, None, fade=False)

        if not self.player:
            self.player = Player(self)
        self.addEntity(self.player)

        if saveData:
            self.player.x = saveData.playerX
            self.player.y = saveData.playerY
            self.player.layer = saveData.playerLayer
            self.player.stats = saveData.stats.clone()
            self.saveFlags = dict(saveData.flags)
        else:
            self.player.x, self.player.y = START_POS
            lay = self.map.GetMetaData()['entityLayer']
            self.player.layer = self.map.FindLayerByName(lay)

        self.things.append(HPBar(self))
        self.things.append(MPBar(self))
        self.things.append(EXPBar(self))

        self.camera = Camera(self)
        self.camera.center()
        self.things.append(self.camera)

    def beginNewGameTask(self):
        self.saveFlags = {}
        yield from cabin.sceneTask(self, 'intro')

        yield from self.mapSwitchTask(START_MAP, START_POS, fade = False)
        lay = self.map.GetMetaData()['entityLayer']

        yield from self.initTask()

        # insanely inefficient:
        startImages = window.effects.createBlurImages(self)
        self.draw()
        endImages = window.effects.createBlurImages(self)
        yield from ika.asTask(window.effects.blurFadeTask(self, 50, startImages, endImages))
        window.effects.freeBlurImages(self, startImages)
        window.effects.freeBlurImages(self, endImages)
        yield from self.runTask()

    def readSaves(self):
        saves = []
        index = 0
        while True:
            save = window.saveload.loadGame(index)
            if save is None:
                return saves
            saves.append(save)
            index += 1

    def writeSave(self, index):
        window.saveload.saveGame(index, window.saveload.SaveData.new(
            self.player.stats.clone(),
            dict(self.saveFlags),
            self.mapName,
            self.player.x,
            self.player.y,
            self.player.layer
        ))

    def loadGameTask(self):
        resultRef = [None]
        yield from saveloadmenu.loadMenuTask(self, resultRef, fadeOut=False)
        [result] = resultRef
        if result:
            startImages = window.effects.createBlurImages(self)
            self.saveFlags = {}
            pos = [result.playerX, result.playerY, result.playerLayer]
            yield from self.mapSwitchTask(result.mapName, pos,  fade=False)
            yield from self.initTask(result)
            self.draw()
            endImages = window.effects.createBlurImages(self)
            yield from ika.asTask(window.effects.blurFadeTask(self, 50, startImages, endImages))
            window.effects.freeBlurImages(self, startImages)
            window.effects.freeBlurImages(self, endImages)
            yield from self.runTask()

    def getImage(self, key):
        return self._engine.getImage(key)

    def mapSwitchTask(self, mapName, dest = None, fade = True):
        print("switching to map", mapName)
        if fade:
            self.draw()
            startImages = window.effects.createBlurImages(self)

        self.mapName = mapName

        # all maps load from the maps/ subdirectory
        mapName = 'maps/' + mapName
        self.background = None
        self.mapThings = []
        self.fields = []
        # TODO: Already called in self.map.Switch() below?
        self.map.clearMapEntities()

        # drop the extension, convert slashes to dots, and prepend the maps package
        # ie 'blah/map42.ika-map' becomes 'maps.blah.map42'
        moduleName = mapName[:mapName.rfind('.')].replace('/', '.')
        mapModule = __import__(moduleName, globals(), locals(), [''])
        self.map.Switch(mapName)

        autoExecFunc = mapModule.__dict__.get('AutoExec', None)
        if autoExecFunc is not None:
            autoExecFunc(self)

        metaData = self.map.GetMetaData()

        self.readZones(mapModule)
        self.readEnts(mapModule)
        if self.player:
            self.player.state = self.player.defaultState()
        if dest and self.player:
            if len(dest) == 2:
                self.player.x, self.player.y = dest
                lay = metaData['entityLayer']
                self.player.layer = self.map.FindLayerByName(lay)
            elif len(dest) == 3:
                self.player.x, self.player.y, self.player.layer = dest
            else:
                assert False

            self.camera.center()

        if 'music' in metaData:
            self.playMusic('music/' + metaData['music'])

        if fade:
            self.draw()
            endImages = window.effects.createBlurImages(self)
            yield from ika.asTask(window.effects.blurFadeTask(self, 50, startImages, endImages))
            window.effects.freeBlurImages(self, startImages)
            window.effects.freeBlurImages(self, endImages)

        self.synchTime()

    def warpTask(self, dest):
        self.draw()
        startImage = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

        self.player.direction = self.dir.Down
        self.player.state = self.player.defaultState()
        self.player.startAnimation('stand')
        self.player.animate()

        self.player.x, self.player.y = dest
        self.camera.center()

        self.draw()
        endImage = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

        time = 50
        endTime = self.getTime() + time
        now = self.getTime()
        while now < endTime:
            opacity = (endTime - now) / time
            ika.Video.Blit(endImage, 0, 0)
            ika.Video.TintBlit(startImage, 0, 0, opacity)
            ika.Video.ShowPage()
            yield None
            now = self.getTime()

        ika.Video.FreeImage(startImage)
        ika.Video.FreeImage(endImage)
        self.synchTime()

    def runTask(self):
        try:
            skipCount = 0
            self.nextFrameTime = self.getTime() + self.ticksPerFrame
            while True:
                t = self.getTime()

                # if we're ahead, delay
                if t < self.nextFrameTime:
                    yield from ika.DelayTask(int(self.nextFrameTime - t))

                if controls.cancel():
                    yield from self.pauseTask()

                # Do some thinking
                yield from self.tickTask()

                # if we're behind, and can, skip the frame.  else draw
                if t > self.nextFrameTime and skipCount < MAX_SKIP_COUNT:
                    skipCount += 1
                else:
                    skipCount = 0
                    self.draw()
                    ika.Video.ShowPage()
                    yield None

                self.nextFrameTime += self.ticksPerFrame

        except GameLoseException:
            yield from self.gameOverTask()
            self.killList = self.entities[:]
            self.clearKillQueue()

        except GameWinException:
            yield from ika.asTask(window.effects.fadeOutTask(self, 200, self.draw))
            self.killList = self.entities[:]
            self.clearKillQueue()
            yield from ending.creditsTask(self)

        except GameQuitException:
            self.killList = self.entities[:]
            self.clearKillQueue()
            return # Brython workaround

        brython_generator_bug_workaround = 'blah'

    def draw(self):
        if self.background:
            ika.Video.ScaleBlit(self.background, 0, 0, ika.Video.xres, ika.Video.yres)
            self.map.Render(*range(self.map.layercount))
        else:
            self.map.Render()

        for t in self.things:
            t.draw()
        for t in self.mapThings:
            t.draw()

    def tickTask(self):
        # We let ika do most of the work concerning entity movement.
        # (in particular, collision detection)
        self.map.ProcessEntities()

        # update entities
        for ent in self.entities:
            yield from ent.updateTask()
        self.clearKillQueue()

        # check fields
        rlayer = self.player.layer
        rx = self.player.x
        ry = self.player.y
        rw = self.player.ent.hotwidth
        rh = self.player.ent.hotheight
        for f in self.fields:
            if f.test(rlayer, rx, ry, rw, rh):
                scriptTask  = f.scriptTask
                yield from scriptTask(self)
                break
            brython_generator_bug_workaround = 'blah'

        # update Things.
        # for each thing in each thing list, we update.
        # If the result is true, we delete the thing, else
        # move on.
        for t in (self.things, self.mapThings):
            i = 0
            while i < len(t):
                result = t[i].update()

                if result:  t.pop(i)
                else:       i += 1

    def addEntity(self, ent):
        assert ent not in self.entities

        self.entities.append(ent)
        self.entFromEnt[ent.ent.name] = ent

    def destroyEntity(self, ent):
        ent.x = ent.y = -1000
        ent.stop()
        self.killList.append(ent)

    def addField(self, field):
        assert field not in self.fields
        self.fields.append(field)

    def addThing(self, thing):
        self.things.append(thing)

    def readZones(self, mapModule):
        '''Read all the zones on the map, and create fields.'''
        self.fields = []

        for i in range(self.map.layercount):
            zones = self.map.GetZones(i)
            for (x, y, w, h, scriptTaskName) in zones:
                scriptTask = mapModule.__dict__[scriptTaskName]
                self.addField(window.field.Field.new([x,y,w,h], i, scriptTask))

    def readEnts(self, mapModule):
        '''Grabs all entities from the map, and adds them to the engine.'''

        # making a gamble here: assuming all entities except the player are tied to the map
        if self.player:
            self.killList= self.entities[:]
            self.killList.remove(self.player)
            self.clearKillQueue()

        for entKey in self.map.entities:
            ent = self.map.entities[entKey]
            if ent.spritename in spawnMap:
                self.addEntity(spawnMap[ent.spritename](self, ent))
            elif ent.spritename != PLAYER_SPRITE:
                print('Unknown entity sprite %s.  Ignoring.' % ent.spritename)

    def clearKillQueue(self):
        # it's a bad idea to tweak the entity list in the middle of an iteration,
        # so we queue them up, and nuke them here.
        for ent in self.killList:
            if ent is self.player:
                self.player = None
            ent.ent.x, ent.ent.y = -100,0
            ent.ent.Stop()
            del self.entFromEnt[ent.ent.name]
            self.map.RemoveEntity(ent)
            # brython workaround?
            #self.entities.remove(ent)
            for i, e in enumerate(self.entities):
                if e is ent:
                    del self.entities[i]
                    break

        self.killList = []

    def getTime(self):
        return self._engine.getTime()

    def synchTime(self):
        '''Used to keep the engine from thinking it has to catch up
        after executing an event or something.'''

        self.nextFrameTime = self.getTime()

    def gameOverTask(self):
        c = Caption(self.font, 'G A M E   O V E R', duration=1000000, y=(ika.Video.yres - self.font.height) // 2)
        t = 80
        i = 0
        self.fields = []
        while True:
            i = min(i + 1, t)
            c.update()
            yield from self.tickTask()
            self.draw()

            # darken the screen, draw the game over message:
            o = i * 255 // t
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, window.RGB(0, 0, 0, o))
            c.draw()

            ika.Video.ShowPage()
            yield from ika.DelayTask(4)

            if i == t and controls.attack():
                break

    def pauseTask(self):
        self.draw()
        s = subscreen.PauseScreen(self)
        yield from s.runTask()

        self.synchTime()

    def playMusic(self, fname):
        if fname in self.music:
            m = self.music[fname]
        else:
            m = ika.Sound(fname)
            m.loop = True
            self.music[fname] = m

        self.fader.reset(m)
        if self.fader not in self.things:
            self.things.append(self.fader)
