import ika
import system

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to39():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 5 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map39.ika-map', (x, 38 * 16))
