from browser import window
from entity import OldEntity

class Dynamite(OldEntity):
    def __init__(self, engineRef, sprite):
        self.flagName = sprite.name
        super(Dynamite, self).__init__(engineRef, sprite, None)
        self.invincible = True

        if self.flagName in self.engineRef.saveFlags:
            sprite.x = sprite.y = -100
            self.engineRef.destroyEntity(self)

    def update(self):
        assert self.flagName not in self.__dict__, 'Already have this.  Why are we updating?'
        if self.touches(self.engineRef.player):
            self.engineRef.saveFlags[self.flagName] = 'True'
            self.engineRef.destroyEntity(self)
            self.engineRef.things.append(window.caption.Caption.new(self.engineRef, self.engineRef.font, '~1Got a stick of dynamite!'))
