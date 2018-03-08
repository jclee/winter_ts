
import system
import ika
from yeti import Yeti
from soulreaver import SoulReaver
from thing import Thing
from rune import FireRune
import savedata
import sound

def AutoExec():
    engine = system.engineObj

    if 'fireguard' not in savedata.__dict__:
        engine.mapThings.append(RuneListener())

    if 'firerune' in savedata.__dict__.keys():
        ika.Map.RemoveEntity(ika.Map.entities['demiyeti'])
    else:
        engine.mapThings.append(DeathListener())

def to9():
    yield from system.engineObj.mapSwitchTask('map09.ika-map', (system.engineObj.player.x, 1 * 16))

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the fire rune.'
    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if not self.yeti:
            # have to get the entity here, since it hasn't been created yet
            # in AutoExec. (if we had more time, I'd fix that problem instead of
            # doing this)
            sound.playMusic("music/Competative.xm")
            self.yeti = system.engineObj.entFromEnt[
                ika.Map.entities['demiyeti'].name
                ]
        elif self.yeti.stats.hp == 0:
            if 'nearend' not in savedata.__dict__:
                e = ika.Entity(71, 132, 2, 'firerune.ika-sprite')
                e.name = 'firerune'
                system.engineObj.addEntity(
                    FireRune(e)
                    )
            else:
                sound.playMusic("music/winter.ogg")
                savedata.fireguard = 'True'

            return True

    def draw(self):
        pass

class RuneListener(object):
    def update(self):
        if 'nearend' in savedata.__dict__:
            sound.playMusic('music/resurrection.it')
            y = SoulReaver(ika.Entity(21*16, 13*16, 2, 'soulreaver.ika-sprite'))
            system.engineObj.addEntity(y)
            system.engineObj.mapThings.append(DeathListener(y))
            return True

    def draw(self):
        pass
