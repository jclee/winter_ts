import ika
import snow
import system

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to38():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map38.ika-map', (x, 28 * 16))
    
def to40():
    offset_from = 5 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map40.ika-map', (x, 1 * 16))
    
def to41():
    offset_from = 34 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map41.ika-map', (1 * 16, y))
