import ika
import system
import saveloadmenu
import dir

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')

def to4():
    offset_from = 8 * 16  # first horizontal pos possible
    offset_to = 11 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map04.ika-map', (x, 38 * 16))

def to13():
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 49 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map13.ika-map', (x, 1 * 16))
