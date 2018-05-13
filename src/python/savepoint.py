
from entity import Entity
import xi.effects

import saveloadmenu

class SavePoint(Entity):
    def __init__(self, engineRef, ent):
        Entity.__init__(self, engineRef, ent, None)
        self.isTouching = False
        self.interruptable = False
        self.invincible = True

    def updateTask(self):
        t = self.touches(self.engineRef.player)
        if t and not self.isTouching:
            # bump the player backward, so he's not touching us anymore.
            yield from xi.effects.fadeOutTask(200, draw=self.engineRef.draw)

            p = self.engineRef.player
            p.stats.hp = 999
            p.stats.mp = 999

            delta = self.engineRef.dir.toDelta(self.engineRef.dir.invert(p.direction))
            p.x, p.y = p.x + delta.x * 3, p.y + delta.y * 3

            # TODO: neato fadeout, etc.
            # "Do you wish to save?" "Yes/No"

            self.isTouching = True
            self.engineRef.draw()
            yield from saveloadmenu.saveMenuTask(self.engineRef)
            yield from xi.effects.fadeInTask(50, draw=self.engineRef.draw)
            self.engineRef.synchTime()

        elif not t:
            self.isTouching = False
