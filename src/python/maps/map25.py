
import system
import ika

def to23():
    system.engineObj.mapSwitch('map23.ika-map', (6 * 16, 42 * 16))

def to26():
    offset_from = 50 * 16  # first vertical pos possible
    offset_to = 20 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map26.ika-map', (38 * 16, y))

def to30():
    system.engineObj.mapSwitch('map30.ika-map', (9*16, 21*16))
