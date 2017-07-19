
import system
import savedata
import cabin

def AutoExec():
    system.engine.things.append(CabinListener())
    
def to25():
    system.engine.mapSwitch('map25.ika-map', (39 * 16, 5 * 16))

def to31():
    x = system.engine.player.x + 16
    system.engine.mapSwitch('map31.ika-map', (x, 28 * 16))
    
class CabinListener(object):
    def update(self):
        if 'nearend' not in savedata.__dict__:
            cabin.scene('nearend')
            return True

    def draw(self):
        pass

