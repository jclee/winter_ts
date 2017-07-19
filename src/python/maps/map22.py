
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')

def to21():
    system.engine.mapSwitch('map21.ika-map', (38 * 16, system.engine.player.y))
    
def to50():
    system.engine.mapSwitch('map50.ika-map', (9 * 16, 13 * 16))