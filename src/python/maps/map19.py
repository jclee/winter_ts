
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')
    
def to16():
    offset_from = 44 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map16.ika-map', (1 * 16, y))
    
def to21():
    system.engine.mapSwitch('map21.ika-map', (system.engine.player.x, 38 * 16))