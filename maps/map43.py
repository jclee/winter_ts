
import system

def to2():
    yield from system.engineObj.mapSwitchTask('map02.ika-map', (48 * 16, system.engineObj.player.y))
    
def to44():
    offset_from = 3 * 16  # first horizontal pos possible
    offset_to = 22 * 16  # first horizontal pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map44.ika-map', (1 * 16, y))
