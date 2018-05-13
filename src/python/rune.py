from entity import Entity
from caption import Caption

class _Rune(Entity):

    def __init__(self, engineRef, ent):
        super(_Rune, self).__init__(engineRef, ent, None)
        self.invincible = True
        self.name = self.ent.name

        if self.name in engineRef.saveFlags:
            self.x = -100
            self.engineRef.destroyEntity(self)

    def apply(self):
        self.engineRef.player.calcSpells()

    def updateTask(self):
        if self.touches(self.engineRef.player):
            self.engineRef.destroyEntity(self)
            self.engineRef.addThing(Caption(self.engineRef.font, '~1You got the %s Rune!' % self.element))
            self.engineRef.saveFlags[self.name] = 'True'
            self.apply()
        if False:
            yield None


class WaterRune(_Rune):
    element = property(lambda self: 'Water')


class FireRune(_Rune):
    element = property(lambda self: 'Fire')


class WindRune(_Rune):
    element = property(lambda self: 'Wind')


class CowardRune(_Rune):
    element = property(lambda self: 'Coward')
        
        
class BindingRune(_Rune):
    element = property(lambda self: 'Binding')


class StrengthRune(_Rune):

    def apply(self):
        self.engineRef.player.stats.att += 2

    element = property(lambda self: 'Strength')


class GuardRune(_Rune):

    def apply(self):
        self.engineRef.player.stats.pres += 2
        self.engineRef.player.stats.mres += 2

    element = property(lambda self: 'Guard')


class PowerRune(_Rune):

    def apply(self):
        self.engineRef.player.stats.mag += 2

    element = property(lambda self: 'Power')
