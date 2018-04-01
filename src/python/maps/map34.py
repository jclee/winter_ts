import ika
import system

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def manaPool():
    system.engineObj.player.stats.mp += 1
    if False:
        yield None
    
def to27():
    yield from system.engineObj.mapSwitchTask('map27.ika-map', (6 * 16, 34 * 16))
    
def to35():
    offset_from = 42 * 16  # first vertical pos possible
    offset_to = 11 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map35.ika-map', (x, 23 * 16))

def to38():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map38.ika-map', (28 * 16, y))
