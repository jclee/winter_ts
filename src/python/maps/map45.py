
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    
def to44():
    offset_from = 23 * 16  # first horizontal pos possible
    offset_to = 28 * 16  # first horizontal pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    system.engineObj.mapSwitch('map44.ika-map', (x, 48 * 16)) 
