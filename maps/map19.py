
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    
def to16():
    offset_from = 44 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map16.ika-map', (1 * 16, y))
    
def to21():
    yield from system.engineObj.mapSwitchTask('map21.ika-map', (system.engineObj.player.x, 38 * 16))
