import system
import saveloadmenu
import dir

def to11():
    system.engineObj.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def heal():
    system.engineObj.player.stats.hp = 999
    system.engineObj.player.stats.mp = 999
