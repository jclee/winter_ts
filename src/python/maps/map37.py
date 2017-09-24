import ika
import savedata
import snow
import system

from carnivore import Carnivore

spawned = 0

def AutoExec():
    global spawned
    spawned = 0
    system.engineObj.mapThings.append(snow.Snow(100, velocity=(.4, 1), colour=ika.RGB(255,192,255)))
    system.engineObj.background = ika.Image('gfx/mountains.png')
    
def to36():
    yield from system.engineObj.mapSwitchTask('map36.ika-map', (system.engineObj.player.x, 1 * 16))
    
def releaseAnklebiters():

    global spawned
    
    if not 'dynamite3' in savedata.__dict__.keys() and not spawned:
        
        indeces = ((6,6), (9,6), (12,6), (4, 8), (14, 8), (2, 10), (6, 10), (12, 10), (16, 10),
                   (4,11), (14, 11))
                   
        for i in indeces:
            system.engineObj.addEntity(Carnivore(ika.Entity(i[0]*16+8, i[1]*16, 1, "carnivore.ika-sprite")))
            
        spawned = 1
    if False:
        yield None
