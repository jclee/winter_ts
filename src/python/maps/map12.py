import system
import saveloadmenu
import dir

def to11():
    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def heal():
    system.engine.player.stats.hp = 999
    system.engine.player.stats.mp = 999
