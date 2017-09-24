import ika
import system

def to25():
    offset_from = 20 * 16  # first vertical pos possible
    offset_to = 50 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map25.ika-map', (1 * 16, y))
    
def to27():
    yield from system.engineObj.mapSwitchTask('map27.ika-map', (system.engineObj.player.x, 78 * 16))    
