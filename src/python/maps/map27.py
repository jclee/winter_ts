import ika
import system

def to26():
    yield from system.engineObj.mapSwitchTask('map26.ika-map', (system.engineObj.player.x, 1 * 16))    
    
def to28():
    offset_from = 33 * 16  # first vertical pos possible
    offset_to = 13 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map28.ika-map', (x, 28 * 16))

def to29():
    offset_from = 22 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map29.ika-map', (1 * 16, y))

def to34():
    yield from system.engineObj.mapSwitchTask('map34.ika-map', (74 * 16, 6.5 * 16))
    
