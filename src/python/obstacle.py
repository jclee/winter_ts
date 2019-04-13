'''Contains entities that are obstructions in the player's path.
Given the proper skill or item, the player can cross these.
'''

from browser import window
import ika

from entity import OldEntity

class _Obstacle(OldEntity):
    def __init__(self, engineRef, sprite, anim = None):
        self.flagName = sprite.name
        OldEntity.__init__(self, engineRef, sprite, anim)
        self.invincible = True

        if self.flagName in engineRef.saveFlags:
            self.remove()

    def remove(self):
        self.sprite.x = self.sprite.y = -100
        self.engineRef.destroyEntity(self)

    def update(self):
        pass

class IceWall(_Obstacle):
    '''
    Not very exciting.  The entity's type is all the information
    we need.
    '''

    def isKind(self, kind):
        return kind == 'IceWall' or super(IceWall, self).isKind(kind)

class Gap(_Obstacle):
    '''A big empty hole. :P'''

    def isKind(self, kind):
        return kind == 'Gap' or super(Gap, self).isKind(kind)

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

    def __init__(self, engineRef, sprite):
        _Obstacle.__init__(self, engineRef, sprite, self._anim)
        self.startAnimation('default')

    def isKind(self, kind):
        return kind == 'IceChunks' or super(IceChunks, self).isKind(kind)

    def remove(self):
        self.freeze()
        _Obstacle.remove(self)

    def freeze(self):
        lay = self.sprite.layer
        tx = self.sprite.x // 16
        ty = self.sprite.y // 16
        for y in range(3):
            for x in range(3):
                self.engineRef.map.SetTile(x + tx, y + ty, lay, self._frozenTiles[y][x])
                self.engineRef.map.SetObs(x + tx, y + ty, lay, False)

        self.engineRef.saveFlags[self.flagName] = 'True'

class Boulder(_Obstacle):
    def __init__(self, *args):
        _Obstacle.__init__(self, *args)

    def update(self):
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
                self.engineRef.things.append(window.caption.Caption.new(self.engineRef, self.engineRef.font, 'Blew the rock apart!'))
