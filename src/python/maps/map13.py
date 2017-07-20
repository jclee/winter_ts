
import system
import ika
import snow

def AutoExec():
    system.engine.mapThings.append(snow.Snow(4000, velocity=(-1, 1.5)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to7():
    system.engine.mapSwitch('map07.ika-map', (78 * 16, system.engine.player.y))

def to14():
    offset_from = 49 * 16  # first horizontal pos possible
    offset_to = 6 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map14.ika-map', (x, 28 * 16))

def to16():
    system.engine.mapSwitch('map16.ika-map', (1 * 16, system.engine.player.y))
