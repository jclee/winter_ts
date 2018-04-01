
import system
import ika
import savedata
import sound
from yeti import Yeti
from soulreaver import SoulReaver
from thing import Thing
from rune import WindRune

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

    if 'bridge_broken' not in savedata.__dict__:
        for x in range(19, 22):
            ika.Map.SetTile(x, 28, 3, 152)
            ika.Map.SetTile(x, 29, 3, 158)
            ika.Map.SetTile(x, 30, 3, 164)
            ika.Map.entities['break_gap'].x = -100

    if 'windguard' not in savedata.__dict__ and 'nearend' in savedata.__dict__:
        system.engineObj.mapThings.append(RuneListener())


def bridge_break():
    if 'bridge_broken' not in savedata.__dict__:

        sound.playMusic('music/Competative.xm')

        savedata.bridge_broken = 'True'

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

        engine = system.engineObj
        p = engine.player
        p.stop()
        p.layer = 2
        p.ent.specframe = 91
        p._state = lambda: None # keep the player from moving

        engine.draw()
        ika.Video.ShowPage()
        yield from ika.DelayTask(8)

        for y in range(32):
            p.y += 1
            ika.Map.ProcessEntities()
            engine.camera.update()
            engine.draw()
            ika.Video.ShowPage()
            yield from ika.DelayTask(1)

        p.layer = 1

        for y in range(32):
            p.y += 1
            ika.Map.ProcessEntities()
            engine.camera.update()
            engine.draw()
            ika.Video.ShowPage()
            yield from ika.DelayTask(1)

        p.ent.specframe = 92
        t = ika.GetTime() + 80
        while t > ika.GetTime():
            engine.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        p.state = p.standState()

        y = Yeti(engine, ika.Entity(304, 64, 1, 'yeti.ika-sprite'))
        # UBER-YETI
        y.stats.maxhp = 400
        y.stats.hp = y.stats.maxhp
        y.stats.att += 10
        engine.addEntity(y)
        engine.mapThings.append(DeathListener(y))

        engine.synchTime()

def manaPool():
    if 'windrune' in savedata.__dict__ and ('nearend' not in savedata.__dict__ or 'windguard' in savedata.__dict__):
        system.engineObj.player.stats.mp += 1
    if False:
        yield None

def to13():
    yield from system.engineObj.mapSwitchTask('map13.ika-map', (78 * 16, system.engineObj.player.y))

def to17():
    yield from system.engineObj.mapSwitchTask('map17.ika-map', (1 * 16, system.engineObj.player.y))

def to19():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 44 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map19.ika-map', (48 * 16, y))

def toLowerLayer():
    system.engineObj.player.layer = 1
    if False:
        yield None

def toUpperLayer():
    system.engineObj.player.layer = 3
    if False:
        yield None

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the wind rune.'
    def __init__(self, yeti):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            if 'windrune' not in savedata.__dict__:
                e = ika.Entity(304, 304, 1, 'windrune.ika-sprite')
                e.name = 'windrune'
                system.engineObj.addEntity(
                    WindRune(e)
                    )
            else:
                setattr(savedata, 'windguard', 'True')
                
            sound.playMusic('music/winter.ogg')
            return True

    def draw(self):
        pass

class RuneListener(object):
    def update(self):
        if 'nearend' in savedata.__dict__:
            sound.playMusic('music/resurrection.it')
            y = SoulReaver(ika.Entity(19*16, 20*16, 1, 'soulreaver.ika-sprite'))
            system.engineObj.addEntity(y)
            system.engineObj.mapThings.append(DeathListener(y))
            return True

    def draw(self):
        pass
