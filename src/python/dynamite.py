from entity import Entity
from caption import Caption
import savedata

class Dynamite(Entity):
    def __init__(self, engineRef, ent):
        self.flagName = ent.name
        super(Dynamite, self).__init__(engineRef, ent, None)
        self.invincible = True

        if self.flagName in savedata.__dict__:
            ent.x = ent.y = -100
            self.engineRef.destroyEntity(self)

    def updateTask(self):
        assert self.flagName not in self.__dict__, 'Already have this.  Why are we updating?'
        if self.touches(self.engineRef.player):
            setattr(savedata, self.flagName, 'True')
            self.engineRef.destroyEntity(self)
            self.engineRef.things.append(Caption('~1Got a stick of dynamite!'))
        if False:
            yield None
