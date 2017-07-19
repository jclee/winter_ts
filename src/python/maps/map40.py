import ika
import system

from snow import Snow

def AutoExec():
    #system.engine.mapThings.append(Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to39():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 5 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map39.ika-map', (x, 38 * 16))