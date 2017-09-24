
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')

def to19():
    yield from system.engineObj.mapSwitchTask('map19.ika-map', (system.engineObj.player.x, 1 * 16))

def to22():
    yield from system.engineObj.mapSwitchTask('map22.ika-map', (1 * 16, system.engineObj.player.y))
    
def to23():
    yield from system.engineObj.mapSwitchTask('map23.ika-map', (48 * 16, system.engineObj.player.y))

def lowerPath():
    system.engineObj.player.layer = 1
    if False:
        yield None
    
def middlePath():
    system.engineObj.player.layer = 3
    if False:
        yield None

def upperPath():
    system.engineObj.player.layer = 4
    if False:
        yield None
