
import system

def to44():
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 32 * 16  # first horizontal pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map44.ika-map', (63 * 16, y))

def to47():
    yield from system.engineObj.mapSwitchTask('map47.ika-map', (38 * 16, 3.5 * 16))
