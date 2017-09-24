import ika
import snow
import system

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    system.engineObj.mapThings.append(snow.Snow(velocity=(0, 0.5)))

def to6():
    offset_from = 21 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map06.ika-map', (38 * 16, y))

def to13():
    yield from system.engineObj.mapSwitchTask('map13.ika-map', (1 * 16, system.engineObj.player.y))
