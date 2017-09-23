import ika

from enemy import Enemy
import player
import Brain
import animator
import sound
import math
import system
import dir

_ankleBiterAnim = {
    'walk': ((
        animator.makeAnim(range(10, 15), 10),
        animator.makeAnim(range(15, 20), 10),
        animator.makeAnim(range(5,10), 10),
        animator.makeAnim(range(0,5), 10),
        animator.makeAnim(range(10, 15), 10),
        animator.makeAnim(range(15, 20), 10),
        animator.makeAnim(range(10, 15), 10),
        animator.makeAnim(range(15, 20), 10),
        ),
        True
    ),

    'idle': ((
        ((10, 1000),),
        ((15, 1000),),
        ((5, 1000),),
        ((0, 1000),),
        ((10, 1000),),
        ((15, 1000),),
        ((10, 1000),),
        ((15, 1000),),
        ),
        True
    ),

    'attack': ((
        zip(range(30, 33), (30, 20, 15)),
        zip(range(35, 38), (30, 20, 15)),
        zip(range(25, 28), (30, 20, 15)),
        zip(range(20, 23), (30, 20, 15)),
        zip(range(30, 33), (30, 20, 15)),
        zip(range(35, 38), (30, 20, 15)),
        zip(range(30, 33), (30, 20, 15)),
        zip(range(35, 38), (30, 20, 15)),
        ),
        False
    ),

    'hurt': ((
        ((38, 1000),),
        ((33, 1000),),
        ((23, 1000),),
        ((28, 1000),),
        ((38, 1000),),
        ((33, 1000),),
        ((38, 1000),),
        ((33, 1000),),
        ),
        False
    ),

    'die': ((
        ((38, 20),(39, 90)),
        ((33, 20),(34, 90)),
        ((23, 20),(24, 90)),
        ((28, 20),(29, 90)),
        ((38, 20),(39, 90)),
        ((33, 20),(34, 90)),
        ((38, 20),(39, 90)),
        ((33, 20),(34, 90)),
        ),
        False
    ),
}

_attackRange = [
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
    (0, -8, 16, 8),
    (0, 16, 16, 8),
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
]

class AnkleBiter(Enemy):
    def __init__(self, ent):
        Enemy.__init__(self, ent, _ankleBiterAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        self.addMoods(
            (Brain.Attack(1), self.attackMood),
            (Brain.Flee(1), self.passiveMood)
        )

        self.mood = self.passiveMood
        self.stats.maxhp = self.stats.hp = 20
        self.stats.att = 7
        self.stats.exp = 1

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.anklebiterHurt.Play()
        if self.stats.hp < self.stats.maxhp / 2:
            self.mood = self.fleeMood
        return super(AnkleBiter, self).hurtState(int(recoilSpeed * 1.5), recoilDir)

    def die(self, *args):
        # When one dies, the others scatter

        ents = [system.engineObj.entFromEnt[x] for x in
            ika.EntitiesAt(self.x - 50, self.y - 50, 100, 100, self.layer)
            if x in system.engineObj.entFromEnt]
        allies = filter(lambda e: isinstance(e, AnkleBiter) and e.stats.hp > 0, ents)

        for a in allies:
            a.mood = a.fleeMood
            a.state = a.idleState()

        super(AnkleBiter, self).die(*args)

    def attackMood(self):
        # if we want to be uber, we can remove this hack.
        # for now fuckit.  Attack the player!!
        p = system.engineObj.player
        for q in range(5):
            d = dir.fromDelta(p.x - self.x, p.y - self.y)
            dist = math.hypot(p.x - self.x, p.y - self.y)
            if dist < 40:
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                yield self.walkState(d, min(30, dist))

    def fleeMood(self):
        MIN_DIST = 150
        p = system.engineObj.player
        for q in range(5):
            d = dir.fromDelta(p.x - self.x, p.y - self.y)
            dist = math.hypot(p.x - self.x, p.y - self.y)

            if dist > MIN_DIST:
                break

            yield self.walkState(dir.invert[d], MIN_DIST - dist)

        self.mood = self.passiveMood
        yield self.idleState()

    def passiveMood(self):
        p = system.engineObj.player
        self._animator.kill = True
        while True:
            dist = math.hypot(p.x - self.x, p.y - self.y)

            yield self.idleState()

            if dist < 150:
                sound.anklebiterStrike.Play()
                self.mood = self.attackMood
                yield self.idleState()
                break
            brython_generator_bug_workaround = 'blah'

    def idleState(self, *args):
        self._animator.kill = True
        return super(AnkleBiter, self).idleState(*args)

    def walkState(self, dir, dist):
        ox, oy = self.x, self.y
        self.move(dir, dist)
        self.anim = 'walk'
        while self.moving:
            yield None
            if (ox, oy) == (self.x, self.y):
                break
        self.stop()

    def deathState(self, *args, **kwargs):
        sound.anklebiterDie.Play()
        self.anim = 'die'
        return super(AnkleBiter, self).deathState(*args, **kwargs)

    def attackState(self, dir):
        class SpeedSaver(object):
            def __init__(_self): _self.s = self.speed
            def __del__(_self):  self.speed = _self.s
        ss = SpeedSaver()

        self.direction = dir
        self.anim = 'attack'
        self.stop()

        sound.anklebiterStrike.Play()

        self.speed *= 2

        # Winding up for the pounce.  Stop until the animation advances to the
        # next frame.
        while self._animator.index == 0:
            yield None

        self.move(dir, 32)
        while not self._animator.kill:
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return

            yield None
        self.stop()
