import Brain
import sound
from entity import Entity

class GenWrapper(object):
    def __init__(self, gen, *args, **kw):
        self.fun = gen
        self.iter = gen(*args, **kw)

    def __call__(self):
        return next(self.iter)

    def __repr__(self):
        return repr((self.fun, self.iter))

class Enemy(Entity):
    '''
    Enemy baseclass.  Enemies are entities that die.

    Enemies also have a brain.  Unlike the player, the state generators
    are allowed to end, at which point the brain is queried as to what to do
    next.

    Maybe it would be a good idea to send the brain information about why
    it is reconsidering its options.
    '''
    def __init__(self, engineRef, ent, anim, brain):
        Entity.__init__(self, engineRef, ent, anim)
        self.brain = brain
        self.state = self.idleState()
        self.stats.hp = 15
        self._mood = None

        # Describe how we implement various moods
        self.actions = {
            Brain.Attack : self.idleState,
            Brain.Flee : self.idleState
        }

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value):
        if value is None:
            self._mood = None
            return
        self._mood = GenWrapper(value)

    def addMood(self, mood, func):
        self.brain.moods.append(mood)
        self.actions[mood] = func

    def addMoods(self, *args):
        for m, f in args:
            self.addMood(m, f)

    def think(self):
        try:
            if self.mood is None:
                raise StopIteration

            s = self.mood()
            self.state = s
        except StopIteration:
            #self.interruptable = True
            action = self.brain.think()
            m = self.actions[action]
            self.mood = m
            self.state = self.mood()

    def die(self, recoilSpeed = 0, recoilDir = None):
        self._mood = None
        self.brain = None
        self.interruptable = True
        self.state = self.deathState(recoilSpeed, recoilDir)
        self.engineRef.player.giveXP(self.stats.exp)
        #self.engineRef.player.stats.mp += self.stats.exp # MP Regen for the player.

    def deathState(self, recoilSpeed, recoilDir):
        self.invincible = True
        self.interruptable = False

        if recoilDir is None:
            recoilDir = self.direction # bleh

        # do the hurt animation
        dummy = self.hurtState(recoilSpeed, recoilDir)

        # let it go for a moment
        yield next(dummy)

        self.stats.hp = 0

        # take over the animation, then finish the hurt state
        self.anim = 'die'
        for crap in dummy:
            yield None


        self.ent.isobs = False
        # burn cycles until the engine kills us
        while True:
            yield None

    def updateTask(self):
        self.animate()
        if not self._state:
            self.think()
        try:
            next(self._state)
        except StopIteration:
            self.think()
        if False:
            yield None

    def defaultState(self):
        yield None

    def idleState(self, time = 50):
        self.anim = 'idle'
        while time > 0:
            time -= 1
            yield None
        return

    def hurt(self, *args, **kwargs):
        sound.monsterHit.Play()
        super(Enemy,self).hurt(*args, **kwargs)
