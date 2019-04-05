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

    def __init__(self, engineRef, ent):
        _Obstacle.__init__(self, engineRef, ent, self._anim)
        self.startAnimation('default')

    def remove(self):
        self.freeze()
        _Obstacle.remove(self)

    def freeze(self):
        lay = self.layer
        tx = self.x // 16
        ty = self.y // 16
        for y in range(3):
            for x in range(3):
                self.engineRef.map.SetTile(x + tx, y + ty, lay, self._frozenTiles[y][x])
                self.engineRef.map.SetObs(x + tx, y + ty, lay, False)

        self.engineRef.saveFlags[self.flagName] = 'True'

class Boulder(_Obstacle):
    def __init__(self, *args):
        _Obstacle.__init__(self, *args)

    def updateTask(self):
        if self.touches(self.engineRef.player):
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

        if False:
            yield None
