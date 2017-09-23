
import system
import ika
import snow

def AutoExec():
    system.engineObj.mapThings.append(snow.Snow(4000, velocity=(-1, 1.5)))
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to7():
    system.engineObj.mapSwitch('map07.ika-map', (78 * 16, system.engineObj.player.y))

def to14():
    offset_from = 49 * 16  # first horizontal pos possible
    offset_to = 6 * 16  # first horizontal pos possible
    x = system.engineObj.player.x - offset_from + offset_to
    system.engineObj.mapSwitch('map14.ika-map', (x, 28 * 16))

def to16():
    system.engineObj.mapSwitch('map16.ika-map', (1 * 16, system.engineObj.player.y))
