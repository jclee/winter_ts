
import system

def to8():
    yield from system.engineObj.mapSwitchTask('map08.ika-map', (system.engineObj.player.x, 1 * 16))

def to41():
    yield from system.engineObj.mapSwitchTask('map41.ika-map', (system.engineObj.player.x + 16, 38 * 16))
