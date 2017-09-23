'''Contains entities that are obstructions in the player's path.
Given the proper skill or item, the player can cross these.
'''

import ika
import savedata
import system

from entity import Entity
from caption import Caption

class _Obstacle(Entity):
    def __init__(self, ent, anim = None):
        self.flagName = ent.name
        Entity.__init__(self, ent, anim)
        self.invincible = True

        if self.flagName in savedata.__dict__:
            self.remove()

    def remove(self):
        self.x = self.y = -100
        system.engineObj.destroyEntity(self)

    def update(self):
        pass

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
        X = self.x / 16
        Y = self.y / 16
        for y in range(3):
            for x in range(3):
                ika.Map.SetTile(x + X, y + Y, lay, self._frozenTiles[y][x])
                ika.Map.SetObs(x + X, y + Y, lay, False)

        setattr(savedata, self.flagName, 'True')

class Boulder(_Obstacle):
    def __init__(self, *args):
        self.isTouching = False
        _Obstacle.__init__(self, *args)

    def update(self):
        t = self.touches(system.engineObj.player)
        if t and not self.isTouching:
            self.isTouching = True

            # find a stick of TNT
            tnt = [k for k in savedata.__dict__.keys()
                if k.startswith('dynamite')
                and savedata.__dict__[k] == 'True']

            if tnt:
                # TODO: explode animation here
                setattr(savedata, tnt[0], 'False')
                setattr(savedata, self.flagName, 'Broken')
                system.engineObj.destroyEntity(self)
                system.engineObj.things.append(Caption('Blew the rock apart!'))

        else:
            self.isTouching = False
