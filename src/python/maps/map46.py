
import system

def to44():
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 32 * 16  # first horizontal pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map44.ika-map', (63 * 16, y))

def to47():
    system.engineObj.mapSwitch('map47.ika-map', (38 * 16, 3.5 * 16))
