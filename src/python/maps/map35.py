import ika
import system

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to34():
    offset_from = 11 * 16  # first vertical pos possible
    offset_to = 42 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map34.ika-map', (x, 1 * 16))

def to36():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map36.ika-map', (x, 38 * 16))
