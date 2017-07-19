import ika
import system

from snow import Snow

def AutoExec():
    #system.engine.mapThings.append(Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to34():
    offset_from = 11 * 16  # first vertical pos possible
    offset_to = 42 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map34.ika-map', (x, 1 * 16))

def to36():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map36.ika-map', (x, 38 * 16))