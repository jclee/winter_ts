
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')

def to8():
    offset_from = 21 * 16  # first horizontal pos possible
    offset_to = 23 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map08.ika-map', (x, 38 * 16))

def to12():
    system.engine.mapSwitch('map12.ika-map', (10 * 16, 18 * 16))