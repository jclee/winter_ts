
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to21():
    system.engineObj.mapSwitch('map21.ika-map', (38 * 16, system.engineObj.player.y))
    
def to50():
    system.engineObj.mapSwitch('map50.ika-map', (9 * 16, 13 * 16))
