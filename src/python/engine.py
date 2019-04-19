import ika
from browser import window

import sound

FRAME_RATE = 100
MAX_SKIP_COUNT = 10
START_MAP = 'map01.ika-map'
START_POS = (34 * 16, 23  * 16)

spawnMap = {
    # match each sprite name up with the associated class
    'anklebiter.ika-sprite': window.anklebiter.AnkleBiter.new,
    'carnivore.ika-sprite': window.anklebiter.Carnivore.new,
    'devourer.ika-sprite': window.anklebiter.Devourer.new,
    'razormane.ika-sprite': window.razormane.RazorMane.new,
    'dragonpup.ika-sprite': window.razormane.DragonPup.new,
    'hellhound.ika-sprite': window.razormane.HellHound.new,
    'yeti.ika-sprite': window.yeti.Yeti.new,
    'gorilla.ika-sprite': window.yeti.Gorilla.new,
    'soulreaver.ika-sprite': window.yeti.SoulReaver.new,

    'dynamite.ika-sprite': window.dynamite.Dynamite.new,
    'waterrune.ika-sprite': window.rune.WaterRune.new,
    'firerune.ika-sprite': window.rune.FireRune.new,
    'windrune.ika-sprite': window.rune.WindRune.new,
    'cowardrune.ika-sprite': window.rune.CowardRune.new,
    'strengthrune.ika-sprite': window.rune.StrengthRune.new,
    'powerrune.ika-sprite': window.rune.PowerRune.new,
    'guardrune.ika-sprite': window.rune.GuardRune.new,

    'savepoint.ika-sprite': window.savepoint.SavePoint.new,

    'icecave.ika-sprite': window.obstacle.IceWall.new,
    'ice.ika-sprite': window.obstacle.IceWall.new,
    'icechunks.ika-sprite': window.obstacle.IceChunks.new,
    'boulder.ika-sprite': window.obstacle.Boulder.new,
    'vgap.ika-sprite': window.obstacle.Gap.new,
    'hgap.ika-sprite': window.obstacle.Gap.new,
}

class EndGameException(Exception):
    pass

class GameLoseException(EndGameException):
    pass

class GameQuitException(EndGameException):
    pass

class GameWinException(EndGameException):
    pass

class Engine(object):
    '''Core engine thingie.  bleh.'''

    dir = window.Dir

    def __init__(self, engine):
        self.entities = []
        self.killList = []
        self.things = []
        self.mapThings = [] # same as self.things, but is cleared every mapSwitch
        self.fields = []

        # ika sprite "name" : Entity
        self.nameToEntityMap = {}

        self.player = None
        self.background = None

        # framerate regulating stuff:
        self.ticksPerFrame = 100.0 / FRAME_RATE
        self.nextFrameTime = 0

        self._engine = engine
        self.controls = self._engine.controls
        self.map = self._engine.map
        self.font = window.FontClass.new(self._engine, 'system.fnt')
        self.video = self._engine.video
        self.mapName = ''

        self.fader = sound.Crossfader()
        # all music.  Never ever let go. (because I'm lazy)
        self.music = {
            'music/silence': sound.NullSound(),
        }
        self.saveFlags = {}
        self.showSaveMenuAtEndOfTick = False

        def getCameraLocked():
            return self.camera.locked
        self.getCameraLocked = getCameraLocked

        def setCameraLocked(v):
            self.camera.locked = v
        self.setCameraLocked = setCameraLocked

        def addThing(thing):
            self.things.append(thing)
        self.addThing = addThing

        def getEngine():
            return self._engine
        self.getEngine = getEngine

        def getEntities():
            ents = []
            for e in self.nameToEntityMap.values():
                ents.append(e)
            return ents
        self.getEntities = getEntities

        def getEntityForSpriteName(name):
            return self.nameToEntityMap[name]
        self.getEntityForSpriteName = getEntityForSpriteName

        def getMapName():
            return self.mapName
        self.getMapName = getMapName

        def pyAddEntity(ent):
            self.addEntity(ent)
        self.pyAddEntity = pyAddEntity

        def pyDestroyEntity(ent):
            self.destroyEntity(ent)
        self.pyDestroyEntity = pyDestroyEntity

        def pyGivePlayerXP(xp):
            self.player.giveXP(xp)
        self.pyGivePlayerXP = pyGivePlayerXP

        def pyReadSaves():
            return self.readSaves()
        self.pyReadSaves = pyReadSaves

        def pyWriteSave(index):
            self.writeSave(index)
        self.pyWriteSave = pyWriteSave

        def getPlayerEntity():
            return self.player
        self.getPlayerEntity = getPlayerEntity

        def triggerGameLose():
            raise GameLoseException()
        self.triggerGameLose = triggerGameLose

        def triggerGameQuit():
            raise GameQuitException()
        self.triggerGameQuit = triggerGameQuit

        def triggerGameWin():
            raise GameWinException()
        self.triggerGameWin = triggerGameWin

        def getSaveFlag(s):
            if s in self.saveFlags:
                return self.saveFlags[s]
            return ''
        self.getSaveFlag = getSaveFlag

        def setSaveFlag(s, v):
            self.saveFlags[s] = v
        self.setSaveFlag = setSaveFlag

        def setShowSaveMenuAtEndOfTick(v):
            self.showSaveMenuAtEndOfTick = v
        self.setShowSaveMenuAtEndOfTick = setShowSaveMenuAtEndOfTick

    def delayTask(self, time):
        yield from ika.asTask(window.delayTask(time))

    def initTask(self, saveData = None):
        'barf'

        # clean everything
        self.killList = self.entities[:]
        self.clearKillQueue()
        self.things = []
        self.mapThings = []
        self.fields = []

        # ika sprite "name" : Entity
        self.nameToEntityMap = {}

        # TODO - redundant with map switches in beginNewGameTask/loadGameTask? (pos parameter differs...)
        if saveData:
            # evil
            yield from self.mapSwitchTask(saveData.mapName, None, fade=False)
        else:
            yield from self.mapSwitchTask(START_MAP, None, fade=False)

        if not self.player:
            self.player = window.player.Player.new(self)
        self.addEntity(self.player)

        if saveData:
            self.player.sprite.x = saveData.playerX
            self.player.sprite.y = saveData.playerY
            self.player.sprite.layer = saveData.playerLayer
            self.player.stats = saveData.stats.clone()
            self.saveFlags = dict(saveData.flags)
        else:
            self.player.sprite.x, self.player.sprite.y = START_POS
            lay = self.map.GetMetaData()['entityLayer']
            self.player.sprite.layer = self.map.FindLayerByName(lay)

        self.things.append(window.hud.HPBar.new(self))
        self.things.append(window.hud.MPBar.new(self))
        self.things.append(window.hud.EXPBar.new(self))

        self.camera = window.camera.Camera.new(self)
        self.camera.center()
        self.things.append(self.camera)

    def beginNewGameTask(self):
        self.saveFlags = {}
        yield from ika.asTask(window.cabin.sceneTask(self, 'intro'))

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
            self.player.sprite.x,
            self.player.sprite.y,
            self.player.sprite.layer
        ))

    def loadGameTask(self):
        resultRef = [None]
        def setResult(s):
            resultRef[0] = s
        yield from ika.asTask(window.saveloadmenu.loadMenuTask(self, setResult))
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
        self.map.clearSprites()

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
            self.player.setState(self.player.defaultState())
        if dest and self.player:
            if len(dest) == 2:
                self.player.sprite.x, self.player.sprite.y = dest
                lay = metaData['entityLayer']
                self.player.sprite.layer = self.map.FindLayerByName(lay)
            elif len(dest) == 3:
                self.player.sprite.x, self.player.sprite.y, self.player.sprite.layer = dest
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
        startImage = self.video.GrabImage(0, 0, self.video.xres, self.video.yres)

        self.player.direction = self.dir.Down
        self.player.setState(self.player.defaultState())
        self.player.startAnimation('stand')
        self.player.animate()

        self.player.sprite.x, self.player.sprite.y = dest
        self.camera.center()

        self.draw()
        endImage = self.video.GrabImage(0, 0, self.video.xres, self.video.yres)

        time = 50
        endTime = self.getTime() + time
        now = self.getTime()
        while now < endTime:
            opacity = (endTime - now) / time
            self.video.Blit(endImage, 0, 0)
            self.video.TintBlit(startImage, 0, 0, opacity)
            self.video.ShowPage()
            yield None
            now = self.getTime()

        self.video.FreeImage(startImage)
        self.video.FreeImage(endImage)
        self.synchTime()

    def runTask(self):
        try:
            skipCount = 0
            self.nextFrameTime = self.getTime() + self.ticksPerFrame
            while True:
                t = self.getTime()

                # if we're ahead, delay
                if t < self.nextFrameTime:
                    yield from self.delayTask(int(self.nextFrameTime - t))

                if self.controls.cancel():
                    yield from self.pauseTask()

                # Do some thinking
                yield from self.tickTask()

                # if we're behind, and can, skip the frame.  else draw
                if t > self.nextFrameTime and skipCount < MAX_SKIP_COUNT:
                    skipCount += 1
                else:
                    skipCount = 0
                    self.draw()
                    self.video.ShowPage()
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
            yield from ika.asTask(window.ending.creditsTask(self))

        except GameQuitException:
            self.killList = self.entities[:]
            self.clearKillQueue()
            return # Brython workaround

        brython_generator_bug_workaround = 'blah'

    def draw(self):
        if self.background:
            self.video.ScaleBlit(self.background, 0, 0, self.video.xres, self.video.yres)
            self.map.Render(*range(self.map.layercount))
        else:
            self.map.Render()

        for t in self.things:
            t.draw()
        for t in self.mapThings:
            t.draw()

    def tickTask(self):
        # We let ika do most of the work concerning sprite movement.
        # (in particular, collision detection)
        self.map.processSprites()

        # update entities
        for ent in self.entities:
            ent.update()
        self.clearKillQueue()

        # check fields
        rlayer = self.player.sprite.layer
        rx = self.player.sprite.x
        ry = self.player.sprite.y
        rw = self.player.sprite.hotwidth
        rh = self.player.sprite.hotheight
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

        if self.showSaveMenuAtEndOfTick:
            self.showSaveMenuAtEndOfTick = False

            yield from ika.asTask(window.effects.fadeOutTask(self, 50, self.draw))
            self.draw()
            yield from ika.asTask(window.saveloadmenu.saveMenuTask(self))
            yield from ika.asTask(window.effects.fadeInTask(self, 50, self.draw))
            self.synchTime()

    def addEntity(self, ent):
        assert ent not in self.entities

        self.entities.append(ent)
        self.nameToEntityMap[ent.sprite.name] = ent

    def destroyEntity(self, ent):
        ent.sprite.x = -1000
        ent.sprite.y = -1000
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
            self.clearKillQueue()
            for e in self.entities:
                if e is not self.player:
                    self.killList.append(e)
            self.clearKillQueue()

        for spriteKey in self.map.sprites:
            sprite = self.map.sprites[spriteKey]
            if sprite.spritename in spawnMap:
                self.addEntity(spawnMap[sprite.spritename](self, sprite))
            elif sprite.spritename != window.player.PLAYER_SPRITE:
                print('Unknown entity sprite %s.  Ignoring.' % sprite.spritename)

    def clearKillQueue(self):
        # it's a bad idea to tweak the entity list in the middle of an iteration,
        # so we queue them up, and nuke them here.
        for ent in self.killList:
            if ent is self.player:
                self.player = None
            ent.sprite.x, ent.sprite.y = -100,0
            ent.sprite.Stop()
            del self.nameToEntityMap[ent.sprite.name]
            self.map.removeSprite(ent.sprite)
            # brython workaround?
            #self.entities.remove(ent)
            for i, e in enumerate(self.entities):
                if e.sprite.name == ent.sprite.name:
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
        c = window.caption.Caption.new(self, self.font, 'G A M E   O V E R', None, (self.video.yres - self.font.height) // 2, 1000000)
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
            self.video.DrawRect(0, 0, self.video.xres, self.video.yres, window.RGB(0, 0, 0, o))
            c.draw()

            self.video.ShowPage()
            yield from self.delayTask(4)

            if i == t and self.controls.attack():
                break

    def pauseTask(self):
        self.draw()
        s = window.subscreen.PauseScreen.new(self)
        yield from ika.asTask(s.runTask())

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
