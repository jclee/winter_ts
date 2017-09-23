
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    
def to21():
    system.engineObj.mapSwitch('map21.ika-map', (1 * 16, system.engineObj.player.y))

def to24():
    system.engineObj.mapSwitch('map24.ika-map', (48 * 16, 34 * 16))
    
def to25():
    system.engineObj.mapSwitch('map25.ika-map', (54 * 16, 55 * 16))
    
def Tunnel1_1():  system.engineObj.warp((21 * 16, 21 * 16))
def Tunnel1_2():  system.engineObj.warp((31 * 16, 36 * 16))
def Tunnel2_1():  pass
def Tunnel2_2():  pass
def Tunnel3_1():  system.engineObj.warp((6 * 16, 16 * 16))
def Tunnel3_2():  system.engineObj.warp((22 * 16, 27 * 16))
def Tunnel4_1():  system.engineObj.warp((5 * 16, 34 * 16))
def Tunnel4_2():  system.engineObj.warp((30 * 16, 8 * 16))
def Tunnel5_1():  system.engine.warp((18 * 16, 36 * 16))
def Tunnel5_2():  system.engineObj.warp((45 * 16, 44 * 16))
def Tunnel6_1():  system.engineObj.warp((45 * 16, 37 * 16))
def Tunnel6_2():  system.engineObj.warp((6 * 16, 25 * 16))
def Tunnel7_1():  pass
def Tunnel7_2():  pass    
