
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to8():
    offset_from = 21 * 16  # first horizontal pos possible
    offset_to = 23 * 16  # first horizontal pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map08.ika-map', (x, 38 * 16))

def to12():
    yield from system.engineObj.mapSwitchTask('map12.ika-map', (10 * 16, 18 * 16))
