import ika
import system
import saveloadmenu
import dir

import snow

def AutoExec():
    system.engine.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to34():
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map34.ika-map', (1 * 16, y))

def to39():
    offset_from = 6 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map39.ika-map', (x, 1 * 16))
