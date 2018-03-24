
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    
def to21():
    yield from system.engineObj.mapSwitchTask('map21.ika-map', (1 * 16, system.engineObj.player.y))

def to24():
    yield from system.engineObj.mapSwitchTask('map24.ika-map', (48 * 16, 34 * 16))
    
def to25():
    yield from system.engineObj.mapSwitchTask('map25.ika-map', (54 * 16, 55 * 16))
    
def Tunnel1_1():
    yield from system.engineObj.warpTask((21 * 16, 21 * 16))

def Tunnel1_2():
    yield from system.engineObj.warpTask((31 * 16, 36 * 16))

def Tunnel2_1():
    if False:
        yield None

def Tunnel2_2():
    if False:
        yield None

def Tunnel3_1():
    yield from system.engineObj.warpTask((6 * 16, 16 * 16))

def Tunnel3_2():
    yield from system.engineObj.warpTask((22 * 16, 27 * 16))

def Tunnel4_1():
    yield from system.engineObj.warpTask((5 * 16, 34 * 16))

def Tunnel4_2():
    yield from system.engineObj.warpTask((30 * 16, 8 * 16))

def Tunnel5_1():
    yield from system.engine.warpTask((18 * 16, 36 * 16))

def Tunnel5_2():
    yield from system.engineObj.warpTask((45 * 16, 44 * 16))

def Tunnel6_1():
    yield from system.engineObj.warpTask((45 * 16, 37 * 16))

def Tunnel6_2():
    yield from system.engineObj.warpTask((6 * 16, 25 * 16))

def Tunnel7_1():
    if False:
        yield None

def Tunnel7_2():
    if False:
        yield None
