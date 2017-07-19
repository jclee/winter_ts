
import system

def to8():
    system.engine.mapSwitch('map08.ika-map', (1 * 16, system.engine.player.y))
    
def to10():
    system.engine.mapSwitch('map10.ika-map', (system.engine.player.x, 28 * 16))