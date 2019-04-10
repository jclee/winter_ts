from browser import window
import sound
from entity import Entity

class Enemy(Entity):
    '''
    Enemy baseclass.  Enemies are entities that die.

    Enemies also have a brain.  Unlike the player, the state generators
    are allowed to end, at which point the brain is queried as to what to do
    next.

    Maybe it would be a good idea to send the brain information about why
    it is reconsidering its options.
    '''
    def __init__(self, engineRef, sprite, anim):
        Entity.__init__(self, engineRef, sprite, anim)
        self.setState(self.idleState())
        self.stats.hp = 15
        self._mood = None

        self._moods = []

    def setMood(self, gen):
        if gen is None:
            self._mood = None
            return
        self._mood = gen()

    def addMoods(self, moods):
        self._moods += moods

    def think(self):
        try:
            if self._mood is None:
                raise StopIteration

            self.setState(next(self._mood))
        except StopIteration:
            #self.interruptable = True
            n = window.random(0, len(self._moods))
            m = self._moods[n]
            self.setMood(m)
            self.setState(next(self._mood))

    def die(self):
        self._mood = None
        self.interruptable = True
        self.setState(self.deathState())
        self.engineRef.player.giveXP(self.stats.exp)
        #self.engineRef.player.stats.mp += self.stats.exp # MP Regen for the player.

    def deathState(self):
        self.invincible = True
        self.interruptable = False

        recoilSpeed = 0
        recoilDir = None
        if recoilDir is None:
            recoilDir = self.direction # bleh

        # do the hurt animation
        dummy = self.hurtState(recoilSpeed, recoilDir)

        # let it go for a moment
        yield next(dummy)

        self.stats.hp = 0

        # take over the animation, then finish the hurt state
        self.startAnimation('die')
        for crap in dummy:
            yield None


        self.sprite.isobs = False
        # burn cycles until the engine kills us
        while True:
            yield None

    def update(self):
        self.animate()
        if not self._state:
            self.think()
        try:
            next(self._state)
        except StopIteration:
            self.think()

    def defaultState(self):
        yield None

    def idleState(self, time = 50):
        self.startAnimation('idle')
        while time > 0:
            time -= 1
            yield None
        return

    def hurt(self, *args, **kwargs):
        sound.monsterHit.Play()
        super(Enemy,self).hurt(*args, **kwargs)
