
import system
import ika

def AutoExec():
    system.engineObj.background = ika.Image('gfx/mountains.png')
    ika.Map.SetObs(10,3,3,0)

def to16():
    system.engineObj.mapSwitch('map16.ika-map', (38 * 16, system.engineObj.player.y))
    
def Tunnel1_1():
    ika.Map.SetObs(10,3,3,1)
    ika.Map.SetObs(16,7,3,0)
    ika.Map.SetObs(6,14,3,0)
    system.engineObj.warp((16 * 16, 7 * 16))
def Tunnel1_2():  
    ika.Map.SetObs(10,3,3,0)
    ika.Map.SetObs(16,7,3,1)
    system.engineObj.warp((10 * 16, 3 * 16))
def Tunnel2_1():  
    ika.Map.SetObs(6,14,3,1)
    ika.Map.SetObs(15,18,3,0)
    system.engineObj.warp((15 * 16, 18 * 16))
def Tunnel2_2():  
    ika.Map.SetObs(6,14,3,0)
    ika.Map.SetObs(15,18,3,1)
    system.engineObj.warp((6 * 16, 14 * 16))

def Around1():   
    system.engineObj.warp((1.5 * 16, 15 * 16))
    
def Around2():
    system.engineObj.warp((18.5 * 16, 18 * 16))
    
