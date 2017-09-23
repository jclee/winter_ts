import ika
import system
import savedata
import cabin

from yeti import Yeti
import snow


def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(velocity=(0, 0.5)))
    if 'cowardrune' not in savedata.__dict__:
        system.engineObj.things.append(RuneListener())

def to2():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 38 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map02.ika-map', (48 * 16, y))

def to49():
    system.engineObj.mapSwitch('map49.ika-map', (14 * 16, 23 * 16))

class RuneListener(object):
    def update(self):
        if 'waterguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__ and 'windguard' in savedata.__dict__:
            system.engineObj.addEntity(
                Yeti(ika.Entity(35 * 16, 19 * 16, system.engineObj.player.layer, 'yeti.ika-sprite')))        
            return True

    def draw(self):
        pass
