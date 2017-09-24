import ika
import system
import savedata
import sound
from thing import Thing
from yeti import Yeti
from soulreaver import SoulReaver

import snow

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(8000, velocity=(-.2, 3)))
    if 'waterrune' not in savedata.__dict__:
        system.engineObj.things.append(RuneListener())
    if 'nearend' in savedata.__dict__:
        system.engineObj.things.append(RuneListener())

def to3():
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map03.ika-map', (x, 1 * 16))

def to5():
    yield from system.engineObj.mapSwitchTask('map05.ika-map', (10 * 16, 19 * 16))

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
            y = SoulReaver(ika.Entity(15* 16, 17 * 16, system.engineObj.player.layer, 'soulreaver.ika-sprite'))
            system.engineObj.addEntity(y)
            system.engineObj.mapThings.append(DeathListener(y))
            return True
        elif 'waterrune' in savedata.__dict__ and 'nearend' not in savedata.__dict__:
            system.engineObj.addEntity(
                Yeti(ika.Entity(15* 16, 32 * 16, system.engineObj.player.layer, 'yeti.ika-sprite'))
                )
            return True

    def draw(self):
        pass
