
import system
import ika
from snow import Snow

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))

def to6():
    offset_from = 21 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map06.ika-map', (38 * 16, y))

def to13():
    system.engine.mapSwitch('map13.ika-map', (1 * 16, system.engine.player.y))
