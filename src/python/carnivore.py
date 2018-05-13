
from anklebiter import AnkleBiter, _attackRange
import player

class Carnivore(AnkleBiter):
    def __init__(self, *args):
        super(Carnivore, self).__init__(*args)
        self.speed = 100
        self.stats.maxhp = 50
        self.stats.hp = 50
        self.stats.att = 16
        self.stats.exp = 10

    def attackState(self, dir):
        oldSpeed = self.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.speed = oldSpeed
        self._onStateExit = restoreVars

        self.direction = dir
        self.startAnimation('attack')
        self.stop()
        self.speed *= 2

        # Winding up for the pounce.  Stop until the animation advances to the
        # next frame.
        for i in range(30):
            yield None

        # force the animator to move on
        self._animator.count = 0

        self.move(dir, 32)
        while self.isAnimating():
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return
            # TODO: hit detection
            yield None

        self.stop()
