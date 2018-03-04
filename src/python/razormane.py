import ika

from enemy import Enemy
import player
import Brain
import animator
import sound
import math
import system
import dir

_razorManeAnim = {
    'walk': ((
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        animator.makeAnim(range(21, 28), 9),
        animator.makeAnim(range(0,7), 9),
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        ),
        True
    ),

    'idle': ((
            ((7, 1000),),
            ((14, 1000),),
            ((21, 1000),),
            ((0, 1000),),
            ((7, 1000),),
            ((14, 1000),),
            ((7, 1000),),
            ((14, 1000),),
        ),
        False
    ),

    'attack': ((
        list(zip(range(35, 37), (30, 20, 15))),
        list(zip(range(42, 44), (30, 20, 15))),
        list(zip(range(28, 30), (30, 20, 15))),
        list(zip(range(49, 51), (30, 20, 15))),
        list(zip(range(35, 37), (30, 20, 15))),
        list(zip(range(42, 44), (30, 20, 15))),
        list(zip(range(35, 37), (30, 20, 15))),
        list(zip(range(42, 44), (30, 20, 15))),
        ),
        False
    ),

    'hurt': ((
        ((44, 1000),),
        ((37, 1000),),
        ((51, 1000),),
        ((30, 1000),),
        ((44, 1000),),
        ((37, 1000),),
        ((44, 1000),),
        ((37, 1000),),
        ),
        False
    ),

    'die': ((
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
        ((51, 20),(52, 90)),
        ((30, 20),(31, 90)),
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
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

class RazorMane(Enemy):
    def __init__(self, ent):
        Enemy.__init__(self, ent, _razorManeAnim, Brain.Brain())

        self.addMoods(
            (Brain.Attack(1), self.stalkMood),
            (Brain.Flee(1), self.passiveMood)
        )

        self.mood = self.passiveMood
        self.speed = 150
        self.stats.maxhp = self.stats.hp = 60
        self.stats.att = 20
        self.stats.exp = 13

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.razorManeHurt.Play()
        if self.stats.hp < self.stats.maxhp // 2:
            self.mood = self.fleeMood
        return super(RazorMane, self).hurtState(recoilSpeed, recoilDir)

    def dieTask(self, *args):
        # When one dies, the others scatter

        ents = [system.engineObj.entFromEnt[x.name] for x in
            ika.Map.EntitiesAt(self.x - 50, self.y - 50, 100, 100, self.layer)
            if x.name in system.engineObj.entFromEnt]
        allies = filter(lambda e: isinstance(e, RazorMane) and e.stats.hp > 0, ents)

        for a in allies:
            a.mood = a.fleeMood
            a.state = a.idleState()

        yield from super(RazorMane, self).dieTask(*args)

    def playerDir(self):
        p = system.engineObj.player
        return dir.fromDelta(p.x - self.x - 10, p.y - self.y - 7)

    def playerDist(self):
        p = system.engineObj.player
        return ika.hypot(p.x - self.x - 10, p.y - self.y - 7)

    def attackMood(self):
        for q in range(5):
            d = self.playerDir()
            dist = self.playerDist()
            if dist < 40:
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                yield self.walkState(d, min(30, dist))

    def stalkMood(self):
        DIST = 0
        p = system.engineObj.player
        # be DIST away, if at all possible
        while True:
            d = self.playerDir()
            dist = self.playerDist()

            if dist - DIST > 60:
                # get closer
                n = dist - DIST - 1
                yield self.walkState(d, ika.Random(n // 2, n))

                yield self.idleState(60)
            elif dist < DIST:
                # fall back

                yield self.walkState(dir.invert[d], min(80, DIST - dist))
                self.direction = d
                yield self.idleState(60)
            else:
                self.mood = self.attackMood
                yield self.idleState(1)

    def fleeMood(self):
        MIN_DIST = 150
        for q in range(5):
            d = self.playerDir()
            dist = self.playerDist()

            if dist > MIN_DIST:
                break

            yield self.walkState(dir.invert[d], MIN_DIST - dist)

        self.mood = self.passiveMood
        yield self.idleState()

    def passiveMood(self):
        p = system.engineObj.player
        self._animator.kill = True
        while True:
            dist = self.playerDist()

            yield self.idleState()

            if dist < 150:
                self.mood = self.stalkMood
                yield self.idleState()
                break
            brython_generator_bug_workaround = 'blah'

    def idleState(self, *args):
        self._animator.kill = True
        return super(RazorMane, self).idleState(*args)

    def walkState(self, dir, dist):
        ox, oy = self.x, self.y
        self.move(dir, dist)
        self.anim = 'walk'
        dist *= 100
        while dist > 0:
            dist -= self.speed
            yield None
            if (ox, oy) == (self.x, self.y):
                break

        self.stop()

    def deathState(self, *args, **kwargs):
        sound.razorManeDie.Play()
        self.anim = 'die'
        return super(RazorMane, self).deathState(*args, **kwargs)

    def attackState(self, dir):
        oldSpeed = self.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.speed = oldSpeed
        self._onStateExit = restoreVars

        self.direction = dir
        self.anim = 'attack'
        self.stop()

        sound.razorManeStrike.Play()

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
