from browser import window
import ika
from entity import Entity

import saveloadmenu

class SavePoint(Entity):
    def __init__(self, engineRef, sprite):
        Entity.__init__(self, engineRef, sprite, None)
        self.interruptable = False
        self.invincible = True

    def updateTask(self):
        if self.touches(self.engineRef.player):
            p = self.engineRef.player
            p.stats.hp = 999
            p.stats.mp = 999

            # bump the player backward, so he's not touching us anymore.
            delta = self.engineRef.dir.toDelta(self.engineRef.dir.invert(p.direction))
            p.x, p.y = p.x + delta.x * 3, p.y + delta.y * 3

            self.engineRef.showSaveMenuAtEndOfTick = True

        if False:
            yield None
