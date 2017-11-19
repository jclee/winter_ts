
from enemy import Enemy
from player import Player
import ika
import Brain
import animator
import system
import sound
import math
import dir

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
        animator.makeAnim(range(8, 14), 15),
        animator.makeAnim(range(15, 21), 15),
        animator.makeAnim(range(22, 28), 15),
        animator.makeAnim(range(1, 7), 15),
        animator.makeAnim(range(8, 14), 15),
        animator.makeAnim(range(15, 21), 15),
        animator.makeAnim(range(8, 14), 15),
        animator.makeAnim(range(15, 21), 15),
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

    'attack': ((
        ((35, 25), (36, 10), (37, 20)),
        ((42, 25), (43, 10), (44, 20)),
        ((49, 25), (50, 10), (51, 20)),
        ((28, 25), (29, 10), (30, 20)),
        ((35, 25), (36, 10), (37, 20)),
        ((42, 25), (43, 10), (44, 20)),
        ((35, 25), (36, 10), (37, 20)),
        ((42, 25), (43, 10), (44, 20)),
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
    def __init__(self, ent):
        Enemy.__init__(self, ent, _anim, Brain.Brain())
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
        return super(Yeti, self).hurtState(dist * 2 // 3, dir)

    def attackMood(self):
        # if we want to be uber, we can remove this hack.
        # for now fuckit.  Attack the player!!
        p = system.engineObj.player
        for q in range(5):
            # compensate for the yeti's gigantic sprite:
            sx = self.x + 16
            sy = self.y + 16
            d = dir.fromDelta(p.x - sx, p.y - sy)
            dist = ika.hypot(p.x - sx, p.y - sy)
            if dist < 50:
                pass
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                yield self.walkState(d, min(90, dist))

    def passiveMood(self):
        p = system.engineObj.player
        self._animator.kill = True
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
        self.anim = 'die'
        return super(Yeti, self).deathState(*args, **kwargs)

    def walkState(self, dir, dist):
        self.move(dir, dist)
        self.anim = 'walk'
        dist *= 100
        while dist > 0:
            dist -= self.speed
            yield None
        self.stop()

    def attackState(self, dir):
        class Saver(object):
            def __init__(_self):        _self.i = self.interruptable
            def __del__(_self):         self.interruptable = _self.i

        saver = Saver()

        self.direction = dir
        self.anim = 'attack'
        self.stop()

        sound.yetiStrike[self.stats.ind].Play()

        self.interruptable = False

        # Wind up.  Hold up a sec.
        while self._animator.index < 2:
            yield None

        self.move(dir, 6)
        while not self._animator.kill:
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if isinstance(e, Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 350, self.direction)
                    yield None
                    break
                brython_generator_bug_workaround = 'blah'

            yield None

        self.stop()

        del saver

        self.state = self.idleState(10)
        yield None
