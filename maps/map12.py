import system
import saveloadmenu
import dir

def to11():
    yield from system.engineObj.mapSwitchTask('map11.ika-map', (23 * 16, 17 * 16))

# Unused?
def heal():
    system.engineObj.player.stats.hp = 999
    system.engineObj.player.stats.mp = 999
    if False:
        yield None
