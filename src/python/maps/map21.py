
import system
import ika

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')

def to19():
    system.engine.mapSwitch('map19.ika-map', (system.engine.player.x, 1 * 16))

def to22():
    system.engine.mapSwitch('map22.ika-map', (1 * 16, system.engine.player.y))
    
def to23():
    system.engine.mapSwitch('map23.ika-map', (48 * 16, system.engine.player.y))

def lowerPath():
    system.engine.player.layer = 1
    
def middlePath():
    system.engine.player.layer = 3

def upperPath():
    system.engine.player.layer = 4