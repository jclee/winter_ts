
import system

def to30():
    x = system.engineObj.player.x - 160
    yield from system.engineObj.mapSwitchTask('map30.ika-map', (6 * 16 + x, 16))

def to32():
    # no adjustment here on purpose
    yield from system.engineObj.mapSwitchTask('map32.ika-map', (25 * 16, 38 * 16))
