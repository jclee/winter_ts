
import system
import snow

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(velocity=(0, 0.5)))
    
def to6():
    offset_from = 29 * 16  # first vertical pos possible
    offset_to = 3 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map06.ika-map', (1 * 16, y))

def to9():
    yield from system.engineObj.mapSwitchTask('map09.ika-map', (28 * 16, system.engineObj.player.y))

def to11():
    offset_from = 23 * 16  # first vertical pos possible
    offset_to = 21 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map11.ika-map', (x, 1 * 16))

def to42():
    yield from system.engineObj.mapSwitchTask('map42.ika-map', (system.engineObj.player.x, 28 * 16))
