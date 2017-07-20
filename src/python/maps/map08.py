
import system
import snow

def AutoExec():
    system.engine.mapThings.append(snow.Snow(velocity=(0, 0.5)))
    
def to6():
    offset_from = 29 * 16  # first vertical pos possible
    offset_to = 3 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map06.ika-map', (1 * 16, y))

def to9():
    system.engine.mapSwitch('map09.ika-map', (28 * 16, system.engine.player.y))

def to11():
    offset_from = 23 * 16  # first vertical pos possible
    offset_to = 21 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map11.ika-map', (x, 1 * 16))

def to42():
    system.engine.mapSwitch('map42.ika-map', (system.engine.player.x, 28 * 16))
