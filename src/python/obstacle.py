'''Contains entities that are obstructions in the player's path.
Given the proper skill or item, the player can cross these.
'''

import ika

from entity import Entity
from caption import Caption

class _Obstacle(Entity):
    def __init__(self, engineRef, ent, anim = None):
        self.flagName = ent.name
        Entity.__init__(self, engineRef, ent, anim)
        self.invincible = True

        if self.flagName in engineRef.saveFlags:
            self.remove()

    def remove(self):
        self.x = self.y = -100
        self.engineRef.destroyEntity(self)

    def updateTask(self):
        if False:
            yield None

class IceWall(_Obstacle):
    '''
    Not very exciting.  The entity's type is all the information
    we need.
    '''
    pass

class Gap(_Obstacle):
    '''A big empty hole. :P'''
    pass

class IceChunks(_Obstacle):
    _anim = {
        'default': ((
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ),
            True
        )
    }

    _frozenTiles = (
        (145, 149, 144),
        (142, 113, 143),
        (139, 148, 138)
    )

    def __init__(self, ent):
        _Obstacle.__init__(self, ent, self._anim)
        self.anim = 'default'

    def remove(self):
        self.freeze()
        _Obstacle.remove(self)

    def freeze(self):
        lay = self.layer
        X = self.x // 16
        Y = self.y // 16
        for y in range(3):
            for x in range(3):
                ika.Map.SetTile(x + X, y + Y, lay, self._frozenTiles[y][x])
                ika.Map.SetObs(x + X, y + Y, lay, False)

        self.engineRef.saveFlags[self.flagName] = 'True'

class Boulder(_Obstacle):
    def __init__(self, *args):
        self.isTouching = False
        _Obstacle.__init__(self, *args)

    def updateTask(self):
        t = self.touches(self.engineRef.player)
        if t and not self.isTouching:
            self.isTouching = True

            # find a stick of TNT
            tnt = [k for k in self.engineRef.saveFlags
                if k.startswith('dynamite')
                and self.engineRef.saveFlags[k] == 'True']

            if tnt:
                # TODO: explode animation here
                self.engineRef.saveFlags[tnt[0]] = 'False'
                self.engineRef.saveFlags[self.flagName] = 'Broken'
                self.engineRef.destroyEntity(self)
                self.engineRef.things.append(Caption(self.engineRef.font, 'Blew the rock apart!'))

        else:
            self.isTouching = False
        if False:
            yield None
