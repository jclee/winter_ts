
import system

def to1():
    system.engineObj.mapSwitch('map01.ika-map', (53 * 16, 4.5 * 16))

def to47():
    y = system.engineObj.player.y
    system.engineObj.mapSwitch('map47.ika-map', (1 * 16, y))
