# TODO DO NOT COMMIT - remove

from browser import window
import ika

from enemy import OldEnemy
import sound

_ankleBiterAnim = {
    'walk': ((
        window.animator.makeAnimRange(10, 15, 10),
        window.animator.makeAnimRange(15, 20, 10),
        window.animator.makeAnimRange(5, 10, 10),
        window.animator.makeAnimRange(0, 5, 10),
        window.animator.makeAnimRange(10, 15, 10),
        window.animator.makeAnimRange(15, 20, 10),
        window.animator.makeAnimRange(10, 15, 10),
        window.animator.makeAnimRange(15, 20, 10),
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

    'windup': ((
        ((30, 1000),),
        ((35, 1000),),
        ((25, 1000),),
        ((20, 1000),),
        ((30, 1000),),
        ((35, 1000),),
        ((30, 1000),),
        ((35, 1000),),
        ),
        True
    ),

    'attack': ((
        ((31, 20), (32, 15)),
        ((36, 20), (37, 15)),
        ((26, 20), (27, 15)),
        ((21, 20), (22, 15)),
        ((31, 20), (32, 15)),
        ((36, 20), (37, 15)),
        ((31, 20), (32, 15)),
        ((36, 20), (37, 15)),
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

class OldAnkleBiter(OldEnemy):
    def __init__(self, engineRef, sprite):
        OldEnemy.__init__(self, engineRef, sprite, _ankleBiterAnim)

        # Test code:
        # Equal probability of attacking or doing nothing.
        self.addMoods([self.attackMood, self.passiveMood])

        self.setMood(self.passiveMood)
        self.stats.maxhp = self.stats.hp = 20
        self.stats.att = 7
        self.stats.exp = 1

    def isKind(self, kind):
        return kind == 'AnkleBiter' or super(OldAnkleBiter, self).isKind(kind)

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.anklebiterHurt.Play()
        if self.stats.hp < self.stats.maxhp // 2:
            self.setMood(self.fleeMood)
        yield from super(OldAnkleBiter, self).hurtState(int(recoilSpeed * 1.5), recoilDir)

    def die(self):
        # When one dies, the others scatter

        ents = [self.engineRef.nameToEntityMap[x.name] for x in
            self.engineRef.map.spritesAt(self.sprite.x - 50, self.sprite.y - 50, 100, 100, self.sprite.layer)
            if x.name in self.engineRef.nameToEntityMap]
        allies = filter(lambda e: e.isKind('AnkleBiter') and e.stats.hp > 0, ents)

        for a in allies:
            a.setMood(a.fleeMood)
            a.setState(a.idleState())

        super(OldAnkleBiter, self).die()

    def attackMood(self):
        # if we want to be uber, we can remove this hack.
        # for now fuckit.  Attack the player!!
        p = self.engineRef.player
        for q in range(5):
            d = self.engineRef.dir.fromDelta(p.sprite.x - self.sprite.x, p.sprite.y - self.sprite.y)
            dist = window.hypot(p.sprite.x - self.sprite.x, p.sprite.y - self.sprite.y)
            if dist < 40:
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                yield self.walkState(d, min(30, dist))

    def fleeMood(self):
        MIN_DIST = 150
        p = self.engineRef.player
        for q in range(5):
            d = self.engineRef.dir.fromDelta(p.sprite.x - self.sprite.x, p.sprite.y - self.sprite.y)
            dist = window.hypot(p.sprite.x - self.sprite.x, p.sprite.y - self.sprite.y)

            if dist > MIN_DIST:
                break

            yield self.walkState(self.engineRef.dir.invert(d), MIN_DIST - dist)

        self.setMood(self.passiveMood)
        yield self.idleState()

    def passiveMood(self):
        p = self.engineRef.player
        self.stopAnimation()
        while True:
            dist = window.hypot(p.sprite.x - self.sprite.x, p.sprite.y - self.sprite.y)

            yield self.idleState()

            if dist < 150:
                sound.anklebiterStrike.Play()
                self.setMood(self.attackMood)
                yield self.idleState()
                break
            brython_generator_bug_workaround = 'blah'

    def idleState(self, *args):
        self.stopAnimation()
        yield from super(OldAnkleBiter, self).idleState(*args)

    def walkState(self, dir, dist):
        ox, oy = self.sprite.x, self.sprite.y
        self.move(dir, dist)
        self.startAnimation('walk')
        while self.isMoving():
            yield None
            if (ox, oy) == (self.sprite.x, self.sprite.y):
                break
        self.stop()

    def deathState(self):
        sound.anklebiterDie.Play()
        self.startAnimation('die')
        yield from super(OldAnkleBiter, self).deathState()

    def attackState(self, dir):
        oldSpeed = self.sprite.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.sprite.speed = oldSpeed
        self._onStateExit = restoreVars

        self.direction = dir
        self.startAnimation('windup')
        self.stop()

        sound.anklebiterStrike.Play()

        self.sprite.speed *= 2

        # Winding up for the pounce.
        for i in range(30):
            yield None

        self.startAnimation('attack')
        self.move(dir, 32)
        while self.isAnimating():
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if e.isKind('Player'):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return

            yield None
        self.stop()
