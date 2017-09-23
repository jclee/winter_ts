
import system
import ika
import savedata

from thing import Thing
from rune import CowardRune

def AutoExec():
    if 'waterguard' in savedata.__dict__ and 'windguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__:
        system.engineObj.mapThings.append(AddRune())
        
def to23():
    system.engineObj.mapSwitch('map23.ika-map', (5 * 16, 5 * 16))
    
def to50():
    system.engineObj.mapSwitch('map50.ika-map', (9 * 16, 13 * 16))
    
class AddRune(object):
    
    def update(self):
        
        e = ika.Entity(315, 320, 1, 'cowardrune.ika-sprite')
        e.name = 'cowardrune'
        system.engineObj.addEntity(CowardRune(e))        
        
        return True
        
    def draw(self):
        pass
        
