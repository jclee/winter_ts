
import system

def to30():
    x = system.engine.player.x - 160
    system.engine.mapSwitch('map30.ika-map', (6 * 16 + x, 16))

def to32():
    # no adjustment here on purpose
    system.engine.mapSwitch('map32.ika-map', (25 * 16, 38 * 16))