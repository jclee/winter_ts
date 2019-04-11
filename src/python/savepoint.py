from browser import window
import ika
from entity import OldEntity

import saveloadmenu

class SavePoint(OldEntity):
    def __init__(self, engineRef, sprite):
        OldEntity.__init__(self, engineRef, sprite, None)
        self.interruptable = False
        self.invincible = True

    def update(self):
        if self.touches(self.engineRef.player):
            p = self.engineRef.player
            p.stats.hp = 999
            p.stats.mp = 999

            # bump the player backward, so he's not touching us anymore.
            delta = self.engineRef.dir.toDelta(self.engineRef.dir.invert(p.direction))
            p.sprite.x, p.sprite.y = p.sprite.x + delta.x * 3, p.sprite.y + delta.y * 3

            self.engineRef.showSaveMenuAtEndOfTick = True
