from browser import window
import ika

from enemy import Enemy
import player
import sound

_razorManeAnim = {
    'walk': ((
        window.animator.makeAnimRange(7, 14, 9),
        window.animator.makeAnimRange(14, 21, 9),
        window.animator.makeAnimRange(21, 28, 9),
        window.animator.makeAnimRange(0, 7, 9),
        window.animator.makeAnimRange(7, 14, 9),
        window.animator.makeAnimRange(14, 21, 9),
        window.animator.makeAnimRange(7, 14, 9),
        window.animator.makeAnimRange(14, 21, 9),
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

    'windup': ((
        ((35, 30),),
        ((42, 30),),
        ((28, 30),),
        ((49, 30),),
        ((35, 30),),
        ((42, 30),),
        ((35, 30),),
        ((42, 30),),
        ),
        False
    ),

    'attack': ((
        ((36, 20),),
        ((43, 20),),
        ((29, 20),),
        ((50, 20),),
        ((36, 20),),
        ((43, 20),),
        ((36, 20),),
        ((43, 20),),
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
    def __init__(self, engineRef, sprite):
        Enemy.__init__(self, engineRef, sprite, _razorManeAnim)

        self.addMoods([self.stalkMood, self.passiveMood])

        self.setMood(self.passiveMood)
        self.sprite.speed = 150
        self.stats.maxhp = self.stats.hp = 60
        self.stats.att = 20
        self.stats.exp = 13

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.razorManeHurt.Play()
        if self.stats.hp < self.stats.maxhp // 2:
            self.setMood(self.fleeMood)
        yield from super(RazorMane, self).hurtState(recoilSpeed, recoilDir)

    def die(self):
        # When one dies, the others scatter

        ents = [self.engineRef.nameToEntityMap[x.name] for x in
            self.engineRef.map.spritesAt(self.sprite.x - 50, self.sprite.y - 50, 100, 100, self.sprite.layer)
            if x.name in self.engineRef.nameToEntityMap]
        allies = filter(lambda e: isinstance(e, RazorMane) and e.stats.hp > 0, ents)

        for a in allies:
            a.setMood(a.fleeMood)
            a.state = a.idleState()

        super(RazorMane, self).die()

    def playerDir(self):
        p = self.engineRef.player
        return self.engineRef.dir.fromDelta(p.sprite.x - self.sprite.x - 10, p.sprite.y - self.sprite.y - 7)

    def playerDist(self):
        p = self.engineRef.player
        return window.hypot(p.sprite.x - self.sprite.x - 10, p.sprite.y - self.sprite.y - 7)

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
        p = self.engineRef.player
        # be DIST away, if at all possible
        while True:
            d = self.playerDir()
            dist = self.playerDist()

            if dist - DIST > 60:
                # get closer
                n = dist - DIST - 1
                yield self.walkState(d, window.random(n // 2, n))

                yield self.idleState(60)
            elif dist < DIST:
                # fall back

                yield self.walkState(self.engineRef.dir.invert(d), min(80, DIST - dist))
                self.direction = d
                yield self.idleState(60)
            else:
                self.setMood(self.attackMood)
                yield self.idleState(1)

    def fleeMood(self):
        MIN_DIST = 150
        for q in range(5):
            d = self.playerDir()
            dist = self.playerDist()

            if dist > MIN_DIST:
                break

            yield self.walkState(self.engineRef.dir.invert(d), MIN_DIST - dist)

        self.setMood(self.passiveMood)
        yield self.idleState()

    def passiveMood(self):
        p = self.engineRef.player
        self.stopAnimation()
        while True:
            dist = self.playerDist()

            yield self.idleState()

            if dist < 150:
                self.setMood(self.stalkMood)
                yield self.idleState()
                break
            brython_generator_bug_workaround = 'blah'

    def idleState(self, *args):
        self.stopAnimation()
        yield from super(RazorMane, self).idleState(*args)

    def walkState(self, dir, dist):
        ox, oy = self.sprite.x, self.sprite.y
        self.move(dir, dist)
        self.startAnimation('walk')
        dist *= 100
        while dist > 0:
            dist -= self.sprite.speed
            yield None
            if (ox, oy) == (self.sprite.x, self.sprite.y):
                break

        self.stop()

    def deathState(self):
        sound.razorManeDie.Play()
        self.startAnimation('die')
        yield from super(RazorMane, self).deathState()

    def attackState(self, dir):
        oldSpeed = self.sprite.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.sprite.speed = oldSpeed
        self._onStateExit = restoreVars

        self.direction = dir
        self.startAnimation('windup')
        self.stop()

        sound.razorManeStrike.Play()

        self.sprite.speed *= 2

        # Winding up for the pounce.
        for i in range(30):
            yield None

        self.startAnimation('attack')
        self.move(dir, 32)
        while self.isAnimating():
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return

            yield None
        self.stop()
