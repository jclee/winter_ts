from browser import window
import ika
from entity import Entity

import saveloadmenu

class SavePoint(Entity):
    def __init__(self, engineRef, ent):
        Entity.__init__(self, engineRef, ent, None)
        self.interruptable = False
        self.invincible = True

    def updateTask(self):
        if self.touches(self.engineRef.player):
            # bump the player backward, so he's not touching us anymore.
            yield from ika.asTask(window.effects.fadeOutTask(self.engineRef, 50, self.engineRef.draw))

            p = self.engineRef.player
            p.stats.hp = 999
            p.stats.mp = 999

            delta = self.engineRef.dir.toDelta(self.engineRef.dir.invert(p.direction))
            p.x, p.y = p.x + delta.x * 3, p.y + delta.y * 3

            # TODO: neato fadeout, etc.
            # "Do you wish to save?" "Yes/No"

            self.engineRef.draw()
            yield from saveloadmenu.saveMenuTask(self.engineRef)
            def draw():
                self.engineRef.draw()
            yield from ika.asTask(window.effects.fadeInTask(self.engineRef, 50, draw))
            self.engineRef.synchTime()
