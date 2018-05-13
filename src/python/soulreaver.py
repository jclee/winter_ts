
from yeti import Yeti, _attackRange

from player import Player
import ika
import sound

class SoulReaver(Yeti):

    def __init__(self, *args):
        super(SoulReaver, self).__init__(*args)
        self.speed = 120
        self.stats.maxhp = 1500
        self.stats.hp = 1500
        self.stats.att = 60
        self.stats.exp = 750
        self.stats.ind = 1
        
    def attackState(self, direc):
        self.direction = direc
        if self.direction == self.engineRef.dir.UpLeft or self.direction == self.engineRef.dir.DownLeft:
            self.direction = self.engineRef.dir.Left
        elif self.direction == self.engineRef.dir.UpRight or self.direction == self.engineRef.dir.DownRight:
            self.direction = self.engineRef.dir.Right

        oldInterruptable = self.interruptable
        def restoreVars(self=self, oldInterruptable=oldInterruptable):
            self.interruptable = oldInterruptable
        self._onStateExit = restoreVars

        self.startAnimation('windup')
        self.stop()
        sound.yetiStrike[self.stats.ind].Play()
        self.interruptable = False

        # Wind up.  Hold up a sec.
        # Show first frame for a bit longer than usual.
        self.stopAnimation()
        for i in range(75):
            yield None
        self.startAnimation('windup')
        for i in range(35):
            yield None

        self.startAnimation('attack')
        self.speed += 800
        self.move(self.direction, 2000)

        for i in range(8):
            self.speed -= (i + 2) * 10
            for e in self.detectCollision(_attackRange[self.direction]):
                if isinstance(e, Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 350, self.direction)
            yield None

        for i in range(30):
            self.speed = max(10, self.speed - 10)
            yield None

        self.stop()

        self.state = self.idleState(10)
        self.speed = 120

        yield None
