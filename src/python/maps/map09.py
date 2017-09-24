
import system

def to8():
    yield from system.engineObj.mapSwitchTask('map08.ika-map', (1 * 16, system.engineObj.player.y))
    
def to10():
    yield from system.engineObj.mapSwitchTask('map10.ika-map', (system.engineObj.player.x, 28 * 16))
