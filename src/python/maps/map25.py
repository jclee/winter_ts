import cabin
import ika
import savedata
import system

def to23():
    yield from system.engineObj.mapSwitchTask('map23.ika-map', (6 * 16, 42 * 16))

def to26():
    offset_from = 50 * 16  # first vertical pos possible
    offset_to = 20 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    yield from system.engineObj.mapSwitchTask('map26.ika-map', (38 * 16, y))

def to30():
    yield from system.engineObj.mapSwitchTask('map30.ika-map', (9*16, 21*16))
    if 'nearend' not in savedata.__dict__:
        yield from cabin.sceneTask('nearend')
