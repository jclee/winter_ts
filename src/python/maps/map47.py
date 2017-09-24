
import system

def to46():
    yield from system.engineObj.mapSwitchTask('map46.ika-map', (25 * 16, 13.5 * 16))
    
def to48():
    offset_from = 81 * 16  # first horizontal pos possible
    offset_to = 18 * 16  # first horizontal pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map48.ika-map', (x, 28 * 16))
    
def to49():
    y = system.engineObj.player.y
    yield from system.engineObj.mapSwitchTask('map49.ika-map', (43 * 16, y))
