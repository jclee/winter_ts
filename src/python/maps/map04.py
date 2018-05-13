import ika
import savedata
import sound
from thing import Thing
from yeti import Yeti
from soulreaver import SoulReaver

import snow

def AutoExec(engineRef):
    engineRef.mapThings.append(snow.Snow(8000, velocity=(-.2, 3)))
    if 'waterrune' not in savedata.__dict__:
        engineRef.mapThings.append(RuneListener(engineRef))
    if 'nearend' in savedata.__dict__:
        engineRef.mapThings.append(RuneListener(engineRef))

def to3(engineRef):
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map03.ika-map', (x, 1 * 16))

def to5(engineRef):
    yield from engineRef.mapSwitchTask('map05.ika-map', (10 * 16, 19 * 16))

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the fire rune.'
    def __init__(self, engineRef, yeti=None):
        self.engineRef = engineRef
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            sound.playMusic("music/winter.ogg")
            savedata.waterguard = 'True'
            return True

    def draw(self):
        pass

class RuneListener(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        if 'nearend' in savedata.__dict__ and 'waterguard' not in savedata.__dict__:
            sound.playMusic("music/resurrection.it")
            y = SoulReaver(ika.Entity(15* 16, 17 * 16, self.engineRef.player.layer, 'soulreaver.ika-sprite'))
            self.engineRef.addEntity(y)
            self.engineRef.mapThings.append(DeathListener(self.engineRef, y))
            return True
        elif 'waterrune' in savedata.__dict__ and 'nearend' not in savedata.__dict__:
            self.engineRef.addEntity(
                Yeti(self.engineRef, ika.Entity(15* 16, 32 * 16, self.engineRef.player.layer, 'yeti.ika-sprite'))
            )
            return True

    def draw(self):
        pass
