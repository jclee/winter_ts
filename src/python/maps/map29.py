import ika
import system

def to27():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 22 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map27.ika-map', (38 * 16, y))