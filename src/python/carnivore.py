
from anklebiter import OldAnkleBiter, _attackRange
import player

class Carnivore(OldAnkleBiter):
    def __init__(self, *args):
        super(Carnivore, self).__init__(*args)
        self.sprite.speed = 100
        self.stats.maxhp = 50
        self.stats.hp = 50
        self.stats.att = 16
        self.stats.exp = 10

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
            # TODO: hit detection
            yield None

        self.stop()
