import ika
import system
import snow

def AutoExec():
    system.engine.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to35():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map35.ika-map', (x, 1 * 16))

def to37():
    system.engine.mapSwitch('map37.ika-map', (system.engine.player.x, 13 * 16))
    
