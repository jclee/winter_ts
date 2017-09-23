
import system

import snow

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(3000, velocity=(-1, 1.5)))

def to1():
    offset_from = 38 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map01.ika-map', (1 * 16, y))

def to3():
    offset_from = 14 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    y = system.engineObj.player.y - offset_from + offset_to
    system.engineObj.mapSwitch('map03.ika-map', (98 * 16, y))

def to6():
    offset_from = 7 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    system.engineObj.mapSwitch('map06.ika-map', (x, 38 * 16))

def to43():
    system.engineObj.mapSwitch('map43.ika-map', (1 * 16, system.engineObj.player.y))
