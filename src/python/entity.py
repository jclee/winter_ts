from browser import window
import ika

class Entity(object):
    'Most every interactive thing in the game is an Entity.'

    # arbitrary, and meaningless for the most part.
    DIST = 48

    def __init__(self, engineRef, sprite, anim):
        'sprite can be None if all of the entity manipulating methods (below) are overridden.'
        self.engineRef = engineRef
        self.sprite = sprite
        self.stats = window.statset.StatSet.new()
        self.stats.hp = 1

        self._animator = window.animator.Animator.new()
        self._anim = anim
        self.direction = self.engineRef.dir.Down # as good as any
        self.interruptable = True # if false, no state changes will occur
        self.invincible = False
        self._state = None
        self._onStateExit = None
        self.setState(self.defaultState())

    def update(self):
        'Main update routine.  Override if you must, use the state mechanism if you can.'
        self.animate()
        if self._state is None:
            self.setState(self.defaultState())
        try:
            next(self._state)
            return
        except StopIteration:
            self.setState(self.defaultState())
            next(self._state)
            return

    def die(self):
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
            self.setState(self.hurtState(recoilSpeed, recoilDir))

    def setState(self, newState):
        if self._onStateExit is not None:
            self._onStateExit()
            self._onStateExit = None
        if self.interruptable or self._state is None:
            self._state = newState

    def defaultState(self):
        while True:
            yield None

    def hurtState(self, recoilSpeed, recoilDir):
        oldSpeed = self.sprite.speed
        oldInvincible = self.invincible
        def restoreVars(self=self, oldSpeed=oldSpeed, oldInvincible=oldInvincible):
            self.sprite.speed = oldSpeed
            self.invincible = oldInvincible
        self._onStateExit = restoreVars

        self.sprite.speed = recoilSpeed
        self.move(recoilDir, 1000000) # just go until I say stop
        self.startAnimation('hurt')

        self.invincible = True
        t = 64
        while True:
            t -= 1
            if t <= 34: self.invincible = oldInvincible
            self.sprite.speed -= t // 8

            yield None

            if t <= 0 or self.sprite.speed <= 0: break

        self.direction = self.engineRef.dir.invert(self.direction)
        self.sprite.Stop()
        yield None

    def detectCollision(self, rect):
        '''
        Returns a list of entities that are within the rect.
        The rect's position is taken as being relative to the
        entity's position.  This is useful for attacks and such.
        '''
        rect = (
            rect[0] + self.sprite.x,
            rect[1] + self.sprite.y,
            rect[2], rect[3],
            self.sprite.layer)

        return [self.engineRef.nameToEntityMap[s.name] for s in
            self.engineRef.map.spritesAt(*rect) if s.name in self.engineRef.nameToEntityMap]

    def touches(self, ent):
        return self.sprite.touches(ent.sprite)

    # Entity methods.  Most everything that involves an ika sprite should be done here.
    def up(self):           self.sprite.moveTo(self.sprite.x, self.sprite.y - self.DIST);    self.direction = self.engineRef.dir.Up
    def down(self):         self.sprite.moveTo(self.sprite.x, self.sprite.y + self.DIST);    self.direction = self.engineRef.dir.Down
    def left(self):         self.sprite.moveTo(self.sprite.x - self.DIST, self.sprite.y);    self.direction = self.engineRef.dir.Left
    def right(self):        self.sprite.moveTo(self.sprite.x + self.DIST, self.sprite.y);    self.direction = self.engineRef.dir.Right
    def upLeft(self):       self.sprite.moveTo(self.sprite.x - self.DIST, self.sprite.y - self.DIST);    self.direction = self.engineRef.dir.UpLeft
    def upRight(self):      self.sprite.moveTo(self.sprite.x + self.DIST, self.sprite.y - self.DIST);    self.direction = self.engineRef.dir.UpRight
    def downLeft(self):     self.sprite.moveTo(self.sprite.x - self.DIST, self.sprite.y + self.DIST);    self.direction = self.engineRef.dir.DownLeft
    def downRight(self):    self.sprite.moveTo(self.sprite.x + self.DIST, self.sprite.y + self.DIST);    self.direction = self.engineRef.dir.DownRight
    def move(self, d, dist = DIST):
        delta = self.engineRef.dir.toDelta(d)
        self.direction = d
        self.sprite.moveTo(int(self.sprite.x + dist * delta.x), int(self.sprite.y + dist * delta.y))

    def isMoving(self):     return self.sprite.isMoving
    def stop(self):         self.sprite.Stop()

    def animate(self):
        self._animator.update()
        self.sprite.specframe = self._animator.curFrame

    def startAnimation(self, name):
        a, loop = self._anim[name]
        self._animator.start(a[self.direction], loop)

    def stopAnimation(self):
        self._animator.stop()

    def isAnimating(self):
        return self._animator.isAnimating

    def getAnimationIndex(self):
        return self._animator.index
