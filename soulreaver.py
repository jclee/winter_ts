
from yeti import Yeti, _attackRange

from enemy import Enemy
from player import Player
import ika
import animator
import system
import sound
import math
import dir


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
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        oldInterruptable = self.interruptable
        def restoreVars(self=self, oldInterruptable=oldInterruptable):
            self.interruptable = oldInterruptable
        self._onStateExit = restoreVars

        self.anim = 'attack'

        attacks = [75]
        speeds = [120]
        extradelay = attacks[ika.Random(0,len(attacks))]
        newspeed = speeds[ika.Random(0,len(speeds))]
        self.stop()

        sound.yetiStrike[self.stats.ind].Play()

        self.interruptable = False

        self._animator.count = extradelay

        # Wind up.  Hold up a sec.
        while self._animator.index < 2:
            yield None

        self.speed += 800
        self.move(self.direction, 2000)

        def thing():
            i = 8
            while i > 0:
                i -= 1
                self.speed -= (10 - i) * 10
                ents = self.detectCollision(_attackRange[self.direction])

                for e in ents:
                    if isinstance(e, Player):
                        d = max(1, self.stats.att - e.stats.pres)
                        e.hurt(d, 350, self.direction)
                        yield None
                        break
                    brython_generator_bug_workaround = 'blah'

                yield None

        for x in thing():
            yield x

        i = 30
        while i > 0:
            i -= 1
            self.speed = max(10, self.speed - 10)
            yield None

        #while not self._animator.kill:
        #    self.speed -= 40
        #    ents = self.detectCollision(_attackRange[dir])

        #    for e in ents:
        #        if isinstance(e, Player):
        #            d = max(1, self.stats.att - e.stats.pres)
        #            e.hurt(d, 350, self.direction)
        #            yield None
        #            break
        #        brython_generator_bug_workaround = 'blah'

        #    yield None

        self.stop()

        self.state = self.idleState(10)

        self.speed = newspeed

        yield None
