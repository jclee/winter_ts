
from anklebiter import OldAnkleBiter, _attackRange
import player

class Devourer(OldAnkleBiter):
    def __init__(self, *args):
        super(Devourer, self).__init__(*args)
        self.sprite.speed = 100
        self.stats.maxhp = 100
        self.stats.hp = self.stats.maxhp
        self.stats.att = 28
        self.stats.exp = 40

    def attackState(self, dir):
        oldSpeed = self.sprite.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.sprite.speed = oldSpeed
        self._onStateExit = restoreVars

        self.direction = dir
        self.startAnimation('windup')
        self.stop()
        self.sprite.speed *= 2

        # Winding up for the pounce.
        for i in range(25):
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
            # TODO: hit detection
            yield None

        self.stop()
