import ika

from animator import Animator
from statset import StatSet

def _temp():
    yield None
GeneratorType = _temp().__class__
del _temp

class Entity(object):
    'Most every interactive thing in the game is an Entity.'

    # arbitrary, and meaningless for the most part.
    DIST = 48

    def __init__(self, engineRef, ent, anim):
        'ent can be None if all of the entity manipulating methods (below) are overridden.'
        self.engineRef = engineRef
        self.ent = ent
        self.stats = StatSet()
        self.stats.hp = 1

        self._animator = Animator()
        self._anim = anim
        self.direction = self.engineRef.dir.Down # as good as any
        self.interruptable = True # if false, no state changes will occur
        self.invincible = False
        self._state = None
        self._onStateExit = None
        self.state = self.defaultState()

    def updateTask(self):
        'Main update routine.  Override if you must, use the state mechanism if you can.'
        self.animate()
        if self._state is None:
            self.state = self.defaultState()
        try:
            next(self._state)
            return
        except StopIteration:
            self.state = self.defaultState()
            next(self._state)
            return
        if False:
            yield None

    def die(self, *args):
        self.engineRef.destroyEntity(self)

    # if recoil is nonzero, the enemy is blown backwards in a direction,
    # at some speed.  The default direction is backwards
    def hurt(self, amount, recoilSpeed = 0, recoilDir = None):
        if self.invincible:
            return

        if recoilDir is None:
            recoilDir = self.engineRef.dir.invert(self.direction)

        if self.stats.hp <= amount:
            self.stats.hp = 0
            self.die()
        else:
            self.stats.hp -= amount
            self.state = self.hurtState(recoilSpeed, recoilDir)

    def _setState(self, newState):
        '''Tries to be psychic.  Generators are recognized, other crap is assumed
        to be a function that returns a generator.'''
        if self._onStateExit is not None:
            self._onStateExit()
            self._onStateExit = None
        if self.interruptable or self._state is None:
            if isinstance(newState, GeneratorType):
                self._state = newState
            elif newState is None:
                self._state = None
            else:
                assert False, 'Entity.state property *must* be a generator!!! (got %s)' % repr(newState)

    state = property(None, _setState)

    def defaultState(self):
        while True:
            yield None

    def hurtState(self, recoilSpeed, recoilDir):
        oldSpeed = self.speed
        oldInvincible = self.invincible
        def restoreVars(self=self, oldSpeed=oldSpeed, oldInvincible=oldInvincible):
            self.speed = oldSpeed
            self.invincible = oldInvincible
        self._onStateExit = restoreVars

        self.speed = recoilSpeed
        self.move(recoilDir, 1000000) # just go until I say stop
        self.startAnimation('hurt')

        self.invincible = True
        t = 64
        while True:
            t -= 1
            if t <= 34: self.invincible = oldInvincible
            self.speed -= t // 8

            yield None

            if t <= 0 or self.speed <= 0: break

        self.direction = self.engineRef.dir.invert(self.direction)
        self.ent.Stop()
        yield None

    def detectCollision(self, rect):
        '''
        Returns a list of entities that are within the rect.
        The rect's position is taken as being relative to the
        entity's position.  This is useful for attacks and such.
        '''
        rect = (
            rect[0] + self.x,
            rect[1] + self.y,
            rect[2], rect[3],
            self.layer)

        return [self.engineRef.entFromEnt[e.name] for e in
            ika.Map.EntitiesAt(*rect) if e.name in self.engineRef.entFromEnt]

    def touches(self, ent):
        return self.ent.Touches(ent.ent)

    # Entity methods.  Most everything that involves an ika entity should be done here.
    def up(self):           self.ent.MoveTo(self.ent.x, self.ent.y - self.DIST);    self.direction = self.engineRef.dir.Up
    def down(self):         self.ent.MoveTo(self.ent.x, self.ent.y + self.DIST);    self.direction = self.engineRef.dir.Down
    def left(self):         self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y);    self.direction = self.engineRef.dir.Left
    def right(self):        self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y);    self.direction = self.engineRef.dir.Right
    def upLeft(self):       self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y - self.DIST);    self.direction = self.engineRef.dir.UpLeft
    def upRight(self):      self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y - self.DIST);    self.direction = self.engineRef.dir.UpRight
    def downLeft(self):     self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y + self.DIST);    self.direction = self.engineRef.dir.DownLeft
    def downRight(self):    self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y + self.DIST);    self.direction = self.engineRef.dir.DownRight
    def move(self, d, dist = DIST):
        delta = self.engineRef.dir.toDelta(d)
        self.direction = d
        self.ent.MoveTo(int(self.ent.x + dist * delta.x), int(self.ent.y + dist * delta.y))

    def isMoving(self):     return self.ent.isMoving
    def stop(self):         self.ent.Stop()

    def animate(self):
        self._animator.update(1)
        self.ent.specframe = self._animator.curFrame

    # properties.  Because they're high in fibre.
    @property
    def x(self):
        return self.ent.x
    @x.setter
    def x(self, value):
        self.ent.x = value

    @property
    def y(self):
        return self.ent.y
    @y.setter
    def y(self, value):
        self.ent.y = value

    @property
    def speed(self):
        return self.ent.speed
    @speed.setter
    def speed(self, value):
        self.ent.speed = value

    @property
    def layer(self):
        return self.ent.layer
    @layer.setter
    def layer(self, value):
        self.ent.layer = value

    def startAnimation(self, name):
        a, loop = self._anim[name]
        self._animator.setAnim(a[self.direction], loop)

    def stopAnimation(self):
        self._animator.kill = True

    def isAnimating(self):
        return not self._animator.kill

    def getAnimationIndex(self):
        return self._animator.index
