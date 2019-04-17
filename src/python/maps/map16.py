import ika
import sound
from yeti import Yeti
from soulreaver import SoulReaver
from thing import Thing

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

    if 'bridge_broken' not in engineRef.saveFlags:
        for x in range(19, 22):
            engineRef.map.SetTile(x, 28, 3, 152)
            engineRef.map.SetTile(x, 29, 3, 158)
            engineRef.map.SetTile(x, 30, 3, 164)
            engineRef.map.sprites['break_gap'].x = -100

    if 'windguard' not in engineRef.saveFlags and 'nearend' in engineRef.saveFlags:
        engineRef.mapThings.append(RuneListener(engineRef))


def bridge_break(engineRef):
    if 'bridge_broken' not in engineRef.saveFlags:

        sound.playMusic('music/Competative.xm')

        engineRef.saveFlags['bridge_broken'] = 'True'

        bridge = (
            (366, 0, 367),
            (372, 0, 373),
            (378, 0, 379)
        )

        for x in range(3):
            engineRef.map.SetTile(x + 19, 28, 3, bridge[0][x])
            engineRef.map.SetTile(x + 19, 29, 3, bridge[1][x])
            engineRef.map.SetTile(x + 19, 30, 3, bridge[2][x])
            engineRef.map.sprites['break_gap'].x = 320

        # This is really cheap.  Probably fragile too.  I'm stepping beyond
        # the game engine and directly twiddling with ika.

        p = engineRef.player
        p.stop()
        p.sprite.layer = 2
        p.sprite.specframe = 91
        p.setState(p.noOpState()) # keep the player from moving

        engineRef.draw()
        engineRef.video.ShowPage()
        yield from engineRef.delayTask(8)

        for y in range(32):
            p.sprite.y += 1
            engineRef.map.processSprites()
            engineRef.camera.update()
            engineRef.draw()
            engineRef.video.ShowPage()
            yield from engineRef.delayTask(1)

        p.sprite.layer = 1

        for y in range(32):
            p.sprite.y += 1
            engineRef.map.processSprites()
            engineRef.camera.update()
            engineRef.draw()
            engineRef.video.ShowPage()
            yield from engineRef.delayTask(1)

        p.sprite.specframe = 92
        t = engineRef.getTime() + 80
        while t > engineRef.getTime():
            engineRef.draw()
            engineRef.video.ShowPage()
            yield None

        p.setState(p.standState())

        y = Yeti(engineRef, engineRef.map.addSprite(304, 64, 1, 'yeti.ika-sprite'))
        # UBER-YETI
        y.stats.maxhp = 400
        y.stats.hp = y.stats.maxhp
        y.stats.att += 10
        engineRef.addEntity(y)
        engineRef.mapThings.append(DeathListener(engineRef, y))

        engineRef.synchTime()

def manaPool(engineRef):
    if 'windrune' in engineRef.saveFlags and ('nearend' not in engineRef.saveFlags or 'windguard' in engineRef.saveFlags):
        engineRef.player.stats.mp += 1
    if False:
        yield None

def to13(engineRef):
    yield from engineRef.mapSwitchTask('map13.ika-map', (78 * 16, engineRef.player.sprite.y))

def to17(engineRef):
    yield from engineRef.mapSwitchTask('map17.ika-map', (1 * 16, engineRef.player.sprite.y))

def to19(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 44 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map19.ika-map', (48 * 16, y))

def toLowerLayer(engineRef):
    engineRef.player.sprite.layer = 1
    if False:
        yield None

def toUpperLayer(engineRef):
    engineRef.player.sprite.layer = 3
    if False:
        yield None

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the wind rune.'
    def __init__(self, engineRef, yeti):
        self.engineRef = engineRef
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            if 'windrune' not in self.engineRef.saveFlags:
                e = self.engineRef.map.addSprite(304, 304, 1, 'windrune.ika-sprite')
                e.name = 'windrune'
                self.engineRef.addEntity(window.rune.WindRune.new(e))
            else:
                self.engineRef.saveFlags['windguard'] = 'True'

            sound.playMusic('music/winter.ogg')
            return True

    def draw(self):
        pass

class RuneListener(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        if 'nearend' in self.engineRef.saveFlags:
            sound.playMusic('music/resurrection.it')
            y = SoulReaver(self.engineRef, self.engineRef.map.addSprite(19*16, 20*16, 1, 'soulreaver.ika-sprite'))
            self.engineRef.addEntity(y)
            self.engineRef.mapThings.append(DeathListener(self.engineRef, y))
            return True

    def draw(self):
        pass
