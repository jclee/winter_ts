from entity import Entity
from caption import Caption
import system
import savedata


class Dynamite(Entity):
    def __init__(self, ent):
        self.flagName = ent.name
        super(Dynamite, self).__init__(ent, None)
        self.invincible = True

        if self.flagName in savedata.__dict__:
            ent.x = ent.y = -100
            system.engineObj.destroyEntity(self)

    def update(self):
        assert self.flagName not in self.__dict__, 'Already have this.  Why are we updating?'
        if self.touches(system.engineObj.player):
            setattr(savedata, self.flagName, 'True')
            system.engineObj.destroyEntity(self)
            system.engineObj.things.append(Caption('~1Got a stick of dynamite!'))
