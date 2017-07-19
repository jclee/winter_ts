import ika
import system
import savedata
import sound
from thing import Thing
from yeti import Yeti
from soulreaver import SoulReaver

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(8000, velocity=(-.2, 3)))
    if 'waterrune' not in savedata.__dict__:
        system.engine.things.append(RuneListener())
    if 'nearend' in savedata.__dict__:
        system.engine.things.append(RuneListener())

def to3():
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map03.ika-map', (x, 1 * 16))

def to5():
    system.engine.mapSwitch('map05.ika-map', (10 * 16, 19 * 16))

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the fire rune.'
    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            sound.playMusic("music/winter.ogg")
            savedata.waterguard = 'True'
            return True

    def draw(self):
        pass
        
class RuneListener(object):
    def update(self):
        if 'nearend' in savedata.__dict__ and 'waterguard' not in savedata.__dict__:
            sound.playMusic("music/resurrection.it")
            y = SoulReaver(ika.Entity(15* 16, 17 * 16, system.engine.player.layer, 'soulreaver.ika-sprite'))
            system.engine.addEntity(y)
            system.engine.mapThings.append(DeathListener(y))
            return True
        elif 'waterrune' in savedata.__dict__ and 'nearend' not in savedata.__dict__:
            system.engine.addEntity(
                Yeti(ika.Entity(15* 16, 32 * 16, system.engine.player.layer, 'yeti.ika-sprite'))
                )
            return True

    def draw(self):
        pass
