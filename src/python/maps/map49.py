
import system

def to1():
    system.engine.mapSwitch('map01.ika-map', (53 * 16, 4.5 * 16))

def to47():
    y = system.engine.player.y
    system.engine.mapSwitch('map47.ika-map', (1 * 16, y))