
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to19():
    system.engineObj.mapSwitch('map19.ika-map', (system.engineObj.player.x, 1 * 16))

def to22():
    system.engineObj.mapSwitch('map22.ika-map', (1 * 16, system.engineObj.player.y))
    
def to23():
    system.engineObj.mapSwitch('map23.ika-map', (48 * 16, system.engineObj.player.y))

def lowerPath():
    system.engineObj.player.layer = 1
    
def middlePath():
    system.engineObj.player.layer = 3

def upperPath():
    system.engineObj.player.layer = 4
