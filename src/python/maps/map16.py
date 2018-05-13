import ika
import sound
from yeti import Yeti
from soulreaver import SoulReaver
from thing import Thing
from rune import WindRune

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

    if 'bridge_broken' not in engineRef.saveFlags:
        for x in range(19, 22):
            ika.Map.SetTile(x, 28, 3, 152)
            ika.Map.SetTile(x, 29, 3, 158)
            ika.Map.SetTile(x, 30, 3, 164)
            ika.Map.entities['break_gap'].x = -100

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
            ika.Map.SetTile(x + 19, 28, 3, bridge[0][x])
            ika.Map.SetTile(x + 19, 29, 3, bridge[1][x])
            ika.Map.SetTile(x + 19, 30, 3, bridge[2][x])
            ika.Map.entities['break_gap'].x = 320

        # This is really cheap.  Probably fragile too.  I'm stepping beyond
        # the game engine and directly twiddling with ika.

        p = engineRef.player
        p.stop()
        p.layer = 2
        p.ent.specframe = 91
        p._state = lambda: None # keep the player from moving

        engineRef.draw()
        ika.Video.ShowPage()
        yield from ika.DelayTask(8)

        for y in range(32):
            p.y += 1
            ika.Map.ProcessEntities()
            engineRef.camera.update()
            engineRef.draw()
            ika.Video.ShowPage()
            yield from ika.DelayTask(1)

        p.layer = 1

        for y in range(32):
            p.y += 1
            ika.Map.ProcessEntities()
            engineRef.camera.update()
            engineRef.draw()
            ika.Video.ShowPage()
            yield from ika.DelayTask(1)

        p.ent.specframe = 92
        t = ika.GetTime() + 80
        while t > ika.GetTime():
            engineRef.draw()
            ika.Video.ShowPage()
            yield None

        p.state = p.standState()

        y = Yeti(engineRef, ika.Entity(304, 64, 1, 'yeti.ika-sprite'))
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
    yield from engineRef.mapSwitchTask('map13.ika-map', (78 * 16, engineRef.player.y))

def to17(engineRef):
    yield from engineRef.mapSwitchTask('map17.ika-map', (1 * 16, engineRef.player.y))

def to19(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 44 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map19.ika-map', (48 * 16, y))

def toLowerLayer(engineRef):
    engineRef.player.layer = 1
    if False:
        yield None

def toUpperLayer(engineRef):
    engineRef.player.layer = 3
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
                e = ika.Entity(304, 304, 1, 'windrune.ika-sprite')
                e.name = 'windrune'
                engineRef.addEntity(
                    WindRune(e)
                    )
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
            y = SoulReaver(ika.Entity(19*16, 20*16, 1, 'soulreaver.ika-sprite'))
            engineRef.addEntity(y)
            engineRef.mapThings.append(DeathListener(self.engineRef, y))
            return True

    def draw(self):
        pass
