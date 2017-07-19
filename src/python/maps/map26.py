import ika
import system

def to25():
    offset_from = 20 * 16  # first vertical pos possible
    offset_to = 50 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map25.ika-map', (1 * 16, y))
    
def to27():
    system.engine.mapSwitch('map27.ika-map', (system.engine.player.x, 78 * 16))    