
from entity import Entity
import xi.effects

import system
import saveloadmenu
import dir

class SavePoint(Entity):
    def __init__(self, ent):
        Entity.__init__(self, ent, None)
        self.isTouching = False
        self.interruptable = False
        self.invincible = True

    def updateTask(self):
        t = self.touches(system.engineObj.player)
        if t and not self.isTouching:
            # bump the player backward, so he's not touching us anymore.
            yield from xi.effects.fadeOutTask(200, draw=system.engineObj.draw)

            p = system.engineObj.player
            p.stats.hp = 999
            p.stats.mp = 999

            dx, dy = dir.delta[dir.invert[p.direction]]
            p.x, p.y = p.x + dx*3, p.y + dy*3

            # TODO: neato fadeout, etc.
            # "Do you wish to save?" "Yes/No"

            self.isTouching = True
            system.engineObj.draw()
            yield from saveloadmenu.saveMenu()
            yield from xi.effects.fadeInTask(50, draw=system.engineObj.draw)
            system.engineObj.synchTime()

        elif not t:
            self.isTouching = False
