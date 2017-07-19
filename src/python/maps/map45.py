
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')
    
def to44():
    offset_from = 23 * 16  # first horizontal pos possible
    offset_to = 28 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map44.ika-map', (x, 48 * 16)) 