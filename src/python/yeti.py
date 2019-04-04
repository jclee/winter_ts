from browser import window

from enemy import Enemy
from player import Player
import ika
import Brain
import sound

_anim = {
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
        True
    ),

    'walk': ((
        window.animator.makeAnimRange(8, 14, 15),
        window.animator.makeAnimRange(15, 21, 15),
        window.animator.makeAnimRange(22, 28, 15),
        window.animator.makeAnimRange(1, 7, 15),
        window.animator.makeAnimRange(8, 14, 15),
        window.animator.makeAnimRange(15, 21, 15),
        window.animator.makeAnimRange(8, 14, 15),
        window.animator.makeAnimRange(15, 21, 15),
        ),
        True
    ),

    'hurt': ((
        ((45, 1000),),
        ((38, 1000),),
        ((31, 1000),),
        ((52, 1000),),
        ((45, 1000),),
        ((38, 1000),),
        ((45, 1000),),
        ((38, 1000),),
        ),
        True
    ),

    'die': ((
        ((38, 30), (39, 90)),
        ((45, 30), (46, 90)),
        ((52, 30), (53, 90)),
        ((31, 30), (32, 90)),
        ((38, 30), (39, 90)),
        ((45, 30), (46, 90)),
        ((38, 30), (39, 90)),
        ((45, 30), (46, 90)),
        ),
        False
    ),

    'windup': ((
        ((35, 25),(36, 10)),
        ((42, 25),(43, 10)),
        ((49, 25),(50, 10)),
        ((28, 25),(29, 10)),
        ((35, 25),(36, 10)),
        ((42, 25),(43, 10)),
        ((35, 25),(36, 10)),
        ((42, 25),(43, 10)),
        ),
        False
    ),

    'attack': ((
        ((37, 20),),
        ((44, 20),),
        ((51, 20),),
        ((30, 20),),
        ((37, 20),),
        ((44, 20),),
        ((37, 20),),
        ((44, 20),),
        ),
        False
    ),
}

_attackRange = (
    (-24, 0, 24, 32),
    (32, 0, 24, 32),
    (-22, -24, 52, 24),
    (-22, 32, 52, 24),
    (-24, 0, 24, 32),
    (32, 0, 24, 32),
    (-24, 0, 24, 32),
    (32, 0, 24, 32),
)

class Yeti(Enemy):
    def __init__(self, engineRef, ent):
        Enemy.__init__(self, engineRef, ent, _anim, Brain.Brain())
        self.speed = 80

        self.addMoods(
            (Brain.Attack(1), self.attackMood),
            (Brain.Passive(1), self.passiveMood)
        )

        self.stats.maxhp = 100
        self.stats.hp = self.stats.maxhp
        self.stats.att = 20
        self.stats.exp = 100
        self.stats.ind = 0

    def hurtState(self, dist, dir):
        if self.stats.hp > 0:
            i = ika.Random(0, len(sound.yetiHurt[self.stats.ind]))
            sound.yetiHurt[self.stats.ind][i].Play()

        self.mood = self.attackMood
        yield from super(Yeti, self).hurtState(dist * 2 // 3, dir)

    def attackMood(self):
        # if we want to be uber, we can remove this hack.
        # for now fuckit.  Attack the player!!
        p = self.engineRef.player
        for q in range(5):
            # compensate for the yeti's gigantic sprite:
            sx = self.x + 16
            sy = self.y + 16
            d = self.engineRef.dir.fromDelta(p.x - sx, p.y - sy)
            dist = ika.hypot(p.x - sx, p.y - sy)
            if dist < 50:
                pass
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                yield self.walkState(d, min(90, dist))

    def passiveMood(self):
        p = self.engineRef.player
        self.stopAnimation()
        while True:
            # compensate for the yeti's gigantic sprite:
            sx = self.x + 16
            sy = self.y + 16
            dist = ika.hypot(p.x - sx, p.y - sy)

            yield self.idleState()

            if dist < 150:
                self.mood = self.attackMood
                yield self.idleState()
                break
            brython_generator_bug_workaround = 'blah'

    def deathState(self, *args, **kwargs):
        sound.yetiDie[self.stats.ind].Play()
        self.startAnimation('die')
        yield from super(Yeti, self).deathState(*args, **kwargs)

    def walkState(self, dir, dist):
        self.move(dir, dist)
        self.startAnimation('walk')
        dist *= 100
        while dist > 0:
            dist -= self.speed
            yield None
        self.stop()

    def attackState(self, dir):
        oldInterruptable = self.interruptable
        def restoreVars(self=self, oldInterruptable=oldInterruptable):
            self.interruptable = oldInterruptable
        self._onStateExit = restoreVars

        self.direction = dir
        self.startAnimation('windup')
        self.stop()
        sound.yetiStrike[self.stats.ind].Play()
        self.interruptable = False

        # Wind up.  Hold up a sec.
        for i in range(35):
            yield None

        self.startAnimation('attack')
        self.move(dir, 6)
        for i in range(20):
            for e in self.detectCollision(_attackRange[dir]):
                if isinstance(e, Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 350, self.direction)
            yield None

        self.stop()

        self.state = self.idleState(10)
        yield None
