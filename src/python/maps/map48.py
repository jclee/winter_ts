
import system

def to47():
    offset_from = 18 * 16  # first horizontal pos possible
    offset_to = 81 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map47.ika-map', (x, 1 * 16))