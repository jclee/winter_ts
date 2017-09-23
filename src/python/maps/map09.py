
import system

def to8():
    system.engineObj.mapSwitch('map08.ika-map', (1 * 16, system.engineObj.player.y))
    
def to10():
    system.engineObj.mapSwitch('map10.ika-map', (system.engineObj.player.x, 28 * 16))
