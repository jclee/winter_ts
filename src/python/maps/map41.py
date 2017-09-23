import ika
import snow
import system

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to39():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 34 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map39.ika-map', (38 * 16, y))
    
def to42():
    system.engineObj.mapSwitch('map42.ika-map', (system.engineObj.player.x - 16, 1 * 16))
