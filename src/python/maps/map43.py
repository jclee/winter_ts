
import system

def to2():
    system.engine.mapSwitch('map02.ika-map', (48 * 16, system.engine.player.y))
    
def to44():
    offset_from = 3 * 16  # first horizontal pos possible
    offset_to = 22 * 16  # first horizontal pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map44.ika-map', (1 * 16, y))
 