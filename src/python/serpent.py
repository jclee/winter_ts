from browser import window

import ika

from anklebiter import AnkleBiter
from carnivore import Carnivore
from enemy import Enemy
from gameover import GameWinException

# arbitrary :D
_idleAnim = window.animator.makeAnim([0, 4, 0, 0, 0, 4, 0, 0, 1, 2, 3, 2, 1, 0], 50)
_biteAnim = window.animator.makeAnimRange(16, 22, 7) # could do some speed-tinkering here.  Make the first and last frames slower than the middle ones.
_stareAnim = window.animator.makeAnim([4, 5, 5, 6, 6, 7, 5, 4], 20)
_roarAnim = window.animator.makeAnim([12, 13, 13, 14, 15, 16, 16, 16, 14, 12], 20)
_deathAnim = window.animator.makeAnimRange(24, 27, 100)
_appearAnim = window.animator.makeAnim([26, 25, 24], 20)
_hurtAnim = ((10, 50),)

_anim = {
    'idle': ((_idleAnim,) * 8, True),
    'bite': ((_biteAnim,) * 8, False),
    'stare': ((_stareAnim,) * 8, False),
    'roar': ((_roarAnim,) * 8, False),
    'die': ((_deathAnim,) * 8, False),
    'appear': ((_appearAnim,) * 8, False),
    'hurt': ((_hurtAnim,) * 8, False),
}

_biteRange = (
    (0, 41, 30, 0),
    (0, 41, 30, 6),
    (0, 41, 30, 20),
    (0, 41, 30, 30),
    (0, 41, 30, 0),
    (0, 41, 30, 0),
)

class Serpent(Enemy):
    def __init__(self, engineRef, sprite):
        Enemy.__init__(self, engineRef, sprite, _anim)

        self.addMoods([self.watchMood])

        self.stats.maxhp = 300
        self.stats.hp = self.stats.maxhp
        self.stats.att = 35
        self.invincible = True

        sprite.mapobs = sprite.entobs = False
        self.bleh = self.watchMood()

    def die(self):
        raise GameWinException()

    def think(self):
        self.setState(next(self.bleh))

    def hurt(self, amount, speed = 0, dir = None):
        Enemy.hurt(self, amount, 0, dir)

    def hurtState(self, *args):
        self.startAnimation('hurt')
        self.invincible = True
        self.interruptable = False
        i = 30
        while i > 0:
            i -= 1
            yield None

        self.interruptable = True

    def watchMood(self):
        '''
        Go left to right, try to vertically align with the player,
        then try to bite.
        Roar every now and again.
        '''
        p = self.engineRef.player

        while True:
            # why is this necessary? O_o
            #self.interruptable = True
            #self._state = None

            for n in range(window.random(1, 8)):
                x = self.sprite.x + self.sprite.hotwidth // 2
                d = self.engineRef.dir.fromDelta(p.sprite.x - x, 0)
                yield self.moveState(d, abs(p.sprite.x - x))

                if window.random(0, 100) < 70:
                    yield self.biteState()

            yield self.roarState()

    def moveState(self, dir, dist):
        self.startAnimation('idle')
        self.move(dir, dist)

        dist *= 100
        while dist > 0:
            dist -= self.sprite.speed
            yield None

    def biteState(self):
        self.startAnimation('bite')
        self.invincible = False

        while self.isAnimating():
            r = _biteRange[self.getAnimationIndex()] + (self.sprite.layer,)
            ents = self.detectCollision(r)
            for e in ents:
                d = max(1, self.stats.att - self.engineRef.player.stats.pres)
                e.hurt(d, 350, self.engineRef.dir.Down)
            yield None

        for i in range(60):
            yield None

        self.invincible = True

    def stareState(self):
        self.startAnimation('stare')
        # TODO: finish this if someone can think of a good idea for
        # what it should do!
        yield None

    def roarState(self):
        # spawn one to five Carnivores to irritate the shit out of the player
        self.startAnimation('roar')

        offsets = [0, 1, 1, 2, 3, 4, 4, 4, 2, 0]
        for wait in range(200):
            offset = offsets[wait // 20]
            self.engineRef.map.xwin += window.random(-offset, offset + 1)
            self.engineRef.map.ywin += window.random(-offset, offset + 1)
            yield None

        for q in range(window.random(1, 4)):
            x, y = 320 + (q * 60), 588
            n = self.engineRef.map.spritesAt(x, y, x + 16, y + 16, self.sprite.layer)

            if not n:
                if window.random(0, 2):
                    e = Carnivore(self.engineRef, self.engineRef.map.addSprite(x, y, self.sprite.layer, 'carnivore.ika-sprite'))
                else:
                    e = AnkleBiter(self.engineRef, self.engineRef.map.addSprite(x, y, self.sprite.layer, 'anklebiter.ika-sprite'))
                self.engineRef.addEntity(e)
                e.setMood(e.attackMood)

        # need to destroy old corpses (a first!)
        for e in self.engineRef.entities:
            if e.stats.hp == 0 and isinstance(e, Enemy):
                self.engineRef.destroyEntity(e)
