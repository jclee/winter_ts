import ika
import system
import snow

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to35():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map35.ika-map', (x, 1 * 16))

def to37():
    yield from system.engineObj.mapSwitchTask('map37.ika-map', (system.engineObj.player.x, 13 * 16))
    
