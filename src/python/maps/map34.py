import ika
import system

import snow

def AutoExec():
    #system.engine.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def manaPool():
    system.engine.player.stats.mp += 1
    
def to27():
    system.engine.mapSwitch('map27.ika-map', (6 * 16, 34 * 16))
    
def to35():
    offset_from = 42 * 16  # first vertical pos possible
    offset_to = 11 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map35.ika-map', (x, 23 * 16))

def to38():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map38.ika-map', (28 * 16, y))
