
import system

def to1():
    yield from system.engineObj.mapSwitchTask('map01.ika-map', (53 * 16, 4.5 * 16))

def to47():
    y = system.engineObj.player.y
    yield from system.engineObj.mapSwitchTask('map47.ika-map', (1 * 16, y))
