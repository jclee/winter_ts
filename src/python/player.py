import ika

import system
import animator
import controls
import sound
import dir
import savedata

from gameover import GameOverException
from statset import StatSet
from caption import Caption

from entity import Entity
from enemy import Enemy
from obstacle import IceWall, IceChunks, Gap


PLAYER_SPRITE = 'protagonist.ika-sprite'

# one entry for each direction
_playerAnim = {
    'walk' : ((
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        animator.makeAnim(range(10, 18), 8),
        animator.makeAnim(range(1, 9), 8),
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        ),
        True
    ),

    'slash': ((
        list(zip(range(63,68), (8,6,4,2,8))),
        list(zip(range(54,59), (8,6,4,2,8))),
        list(zip(range(45,50), (8,6,4,2,8))),
        list(zip(range(36,41), (8,6,4,2,8))),
        list(zip(range(63,68), (8,6,4,2,8))),
        list(zip(range(54,59), (8,6,4,2,8))),
        list(zip(range(63,68), (8,6,4,2,8))),
        list(zip(range(54,59), (8,6,4,2,8))),
        ),
        False
    ),

    'backslash': ((
        list(zip(range(67, 62, -1), (8,6,4,2,8))),
        list(zip(range(58, 53, -1), (8,6,4,2,8))),
        list(zip(range(49, 44, -1), (8,6,4,2,8))),
        list(zip(range(40, 35, -1), (8,6,4,2,8))),
        list(zip(range(67, 62, -1), (8,6,4,2,8))),
        list(zip(range(58, 53, -1), (8,6,4,2,8))),
        list(zip(range(67, 62, -1), (8,6,4,2,8))),
        list(zip(range(58, 53, -1), (8,6,4,2,8))),
        ),
        False
    ),

    'thrust': ((
        list(zip((67, 66, 65), (6, 4, 1000))),
        list(zip((58, 57, 56), (6, 4, 1000))),
        list(zip((49, 48, 47), (6, 4, 1000))),
        list(zip((40, 39, 38), (6, 4, 1000))),
        list(zip((67, 66, 65), (6, 4, 1000))),
        list(zip((58, 57, 56), (6, 4, 1000))),
        list(zip((67, 66, 65), (6, 4, 1000))),
        list(zip((58, 57, 56), (6, 4, 1000))),
        ),
        False
    ),

    'backthrust': ((
        #((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        #((72, 1000),),
        ((81, 1000),),
        ((72, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ),
        True
    ),

    'rend': ((
        list(zip(range(63,68), (12,8,6,2,12))),
        list(zip(range(54,59), (12,8,6,2,12))),
        list(zip(range(45,50), (12,8,6,2,12))),
        list(zip(range(36,41), (12,8,6,2,12))),
        list(zip(range(63,68), (12,8,6,2,12))),
        list(zip(range(54,59), (12,8,6,2,12))),
        list(zip(range(63,68), (12,8,6,2,12))),
        list(zip(range(54,59), (12,8,6,2,12))),
        ),
        False
    ),

    'stand': ((
        ((27, 1000),),
        ((18, 1000),),
        ((9, 1000),),
        ((0, 1000),),
        ((27, 1000),),
        ((18, 1000),),
        ((27, 1000),),
        ((18, 1000),)
        ),
        True
    ),

    'hurt': ((
        ((90, 1000),),
        ((99, 1000),),
        ((72, 1000),),
        ((81, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ),
        True
    ),

    'die': ((
        list(zip((90,  91,  92), (20, 20, 1000))),
        list(zip((99, 100, 101), (20, 20, 1000))),
        list(zip((72,  73,  74), (20, 20, 1000))),
        list(zip((81,  82,  83), (20, 20, 1000))),
        list(zip((90,  91,  92), (20, 20, 1000))),
        list(zip((99, 100, 101), (20, 20, 1000))),
        list(zip((90,  91,  92), (20, 20, 1000))),
        list(zip((99, 100, 101), (20, 20, 1000))),
        ),
        False
    ),

    # temporary:  copy the normal standing frames.
    'magic': ((
        ((27, 1000),),
        ((18, 1000),),
        ((9, 1000),),
        ((0, 1000),),
        ((27, 1000),),
        ((18, 1000),),
        ((27, 1000),),
        ((18, 1000),)
        ),
        True
    ),
}

thrustRange = (
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
    (  6, -27, 10, 27),
    (  6,  17, 10, 12),
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
)

slashRange = (
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-14, -27, 10, 27), ( -4, -27, 10, 27), (  6, -27, 10, 27), ( 16, -27, 10, 27), ( 16, -27, 10, 27)),
    (( 16,  17, 10, 12), ( 16,  17, 10, 12), (  6,  17, 10, 12), ( -4,  17, 10, 12), (-14,  17, 10, 12)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
)

rendRange = (
    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),

    ((-14, -29, 10, 29), ( -4, -29, 10, 29), (  6, -29, 10, 29), ( 16, -29, 10, 29), ( 16, -29, 10, 29)),
    (( 16,  17, 10, 16), ( 16,  17, 10, 16), (  6,  17, 10, 16), ( -4,  17, 10, 16), (-14,  17, 10, 16)),

    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),

    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),
)

galeRange = (
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
    (-8, -8, 24, 8),
    (-8, 16, 24, 8),
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
)

backSlashRange = [x[::-1] for x in slashRange]

initialStats = StatSet(
    maxhp=80,
    hp=80,
    maxmp=40,
    mp=40,
    att=5,
    mag=1,
    pres=1,
    mres=1,
    level=1,
    exp=0,
    next=10)

class Player(Entity):
    def __init__(self, x=0, y=0, layer=0):
        Entity.__init__(self, ika.Entity(x, y, layer, PLAYER_SPRITE), _playerAnim)
        self.state = self.standState()
        self.stats = initialStats.clone()

    def giveXP(self, amount):
        self.stats.exp += amount
        if self.stats.exp >= self.stats.next:
            self.levelUp()

    def levelUp(self):

        sound.achievement.Play()

        while self.stats.exp >= self.stats.next:
            self.stats.maxhp += ika.Random(2, 7)
            self.stats.maxmp += ika.Random(2, 6)

            statlist = []
            for n in range(3):
                if not statlist:
                    statlist = ['att', 'mag', 'pres', 'mres']
                s = statlist[ika.Random(0,len(statlist))]
                self.stats[s]+= 1
                statlist.remove(s)

            self.stats.level += 1

            self.stats.maxhp = min(self.stats.maxhp, 285)
            self.stats.maxmp = min(self.stats.maxmp, 285)
            self.stats.exp -= self.stats.next
            self.stats.next = self.stats.level * (self.stats.level + 1) * 5

        system.engineObj.things.append(Caption('Level %i!' % self.stats.level))

    def calcSpells(self):
        '''
        Figures out what spells the player has access to, based on the
        flags set in the savedata module.
        '''
        bind = len([x for x in savedata.__dict__.keys() if x.startswith('bind')])
        self.stats.rend = 'firerune' in savedata.__dict__
        self.stats.heal = 'waterrune' in savedata.__dict__
        self.stats.gale = 'windrune' in savedata.__dict__
        self.stats.shiver = 'cowardrune' in savedata.__dict__
        self.stats.smoke = self.stats.rend and self.stats.gale and (bind > 0)
        self.stats.vivify = self.stats.rend and self.stats.heal and (bind > 0)
        self.stats.ternion = self.stats.heal and self.stats.gale and self.stats.rend and (bind == 2)

    def defaultState(self):
        return self.standState()

    def standState(self):
        self.stop()
        self.anim = 'stand'
        while True:
            if controls.attack():
                self.state = self.slashState()
            elif controls.rend():
                self.state = self.hearthRendState()
                yield None
            elif controls.gale():
                self.state = self.crushingGaleState()
                yield None
            elif controls.heal():
                self.state = self.healingRainState()
                yield None
            elif controls.shiver():
                self.state = self.shiverState()
                yield None
            elif controls.left() or controls.right() or controls.up() or controls.down():
                self.state = self.walkState()
                next(self._state) # get the walk state started right now.
            yield None

    def walkState(self):
        oldDir = self.direction
        self.anim = 'walk'

        while True:

            if controls.attack():
                self.state = self.slashState()
                yield None
            elif controls.rend():
                self.state = self.hearthRendState()
                yield None
            elif controls.gale():
                self.state = self.crushingGaleState()
                yield None
            elif controls.heal():
                self.state = self.healingRainState()
                yield None
            elif controls.shiver():
                self.state = self.shiverState()
                yield None
            elif controls.left():
                if controls.up():
                    d = dir.UPLEFT
                elif controls.down():
                    d = dir.DOWNLEFT
                else:
                    d = dir.LEFT
            elif controls.right():
                if controls.up():
                    d = dir.UPRIGHT
                elif controls.down():
                    d = dir.DOWNRIGHT
                else:
                    d = dir.RIGHT
            elif controls.up():
                d = dir.UP
            elif controls.down():
                d = dir.DOWN
            else:
                self.state = self.standState()
                yield None

            self.move(d)

            # handle animation and junk
            if d != oldDir:
                self.anim = 'walk'
                self.direction = d
                oldDir = d
            yield None

    def slashState(self):
        self.stop()
        self.anim = 'slash'
        r = slashRange[self.direction]
        backslash = False
        backthrust = False

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash1.Play()

        while not self._animator.kill:
            rect = list(r[self._animator.index]) + [self.layer]
            rect[0] += self.x
            rect[1] += self.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                x = system.engineObj.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(self.stats.att, 120, self.direction)
                    self.giveMPforHit()

            if controls.up() and self.direction == dir.DOWN:  backthrust = True
            elif controls.down() and self.direction == dir.UP:  backthrust = True
            elif controls.left() and self.direction in [dir.RIGHT, dir.UPRIGHT, dir.DOWNRIGHT]:  backthrust = True
            elif controls.right() and self.direction in [dir.LEFT, dir.UPLEFT, dir.DOWNLEFT]:  backthrust = True

            elif controls.attack():
                backslash = True

            yield None

        if backthrust:
            self.state = self.backThrustState()
            yield None
        elif backslash:
            self.state = self.backSlashState()
            yield None
        else:
            # Stall:
            count = 10
            while count > 0:
                count -= 1
                if controls.attack():
                    self.state = self.thrustState()
                yield None

    def backSlashState(self):
        self.stop()
        self.anim = 'backslash'
        r = backSlashRange[self.direction]

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash2.Play()

        while not self._animator.kill:
            rect = list(r[self._animator.index]) + [self.layer]
            rect[0] += self.x
            rect[1] += self.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                x = system.engineObj.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(self.stats.att, 130, self.direction)
                    self.giveMPforHit()

            yield None

        # Stall:
        count = 10
        while count > 0:
            count -= 1
            if controls.rend():
                self.state = self.hearthRendState()
            elif controls.attack():
                self.state = self.thrustState()
            yield None

    def thrustState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        class SpeedSaver(object):
            def __init__(_self):        _self.s = self.speed
            def __del__(_self):         self.speed = _self.s

        ss = SpeedSaver()

        self.anim = 'thrust'
        self.speed += 800
        self.move(self.direction, 1000)

        r = thrustRange[self.direction] + (self.layer,)
        rect = list(r)

        sound.slash3.Play()

        # hack since I need to break out of two levels at once
        def thing():
            i = 8
            while i > 0:
                i -= 1
                self.speed -= (12 - i) * 10

                rect[0] = r[0] + self.x
                rect[1] = r[1] + self.y
                ents = ika.EntitiesAt(*rect)
                for e in ents:
                    x = system.engineObj.entFromEnt[e]
                    if isinstance(x, Enemy) and not x.invincible:
                        x.hurt(int(self.stats.att * 1.5), 300, self.direction)
                        self.giveMPforHit()
                        self.stop()
                        return

                yield None
        for x in thing():
            yield x

        i = 30
        while i > 0:
            i -= 1
            self.speed = max(10, self.speed - 10)
            yield None

        self.stop()

    def backThrustState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        class SpeedSaver(object):
            def __init__(_self):        _self.s = self.speed
            def __del__(_self):         self.speed = _self.s

        ss = SpeedSaver()

        self.anim = 'backthrust'
        self.speed += 400
        self.move(dir.invert[self.direction], 1000)

        i = 8
        while i > 0:
            i -= 1
            self.speed -= 40
            yield None

        i = 30
        thrust = False
        gale = False

        while i > 0:
            i -= 1
            self.speed = max(0, self.speed - 10)
            if controls.attack():
                thrust = True
            elif controls.gale():
                gale = True
            yield None

        self.direction = dir.invert[self.direction]

        if thrust:
            self.state = self.thrustState()
            yield None

        elif gale:
            self.state = self.crushingGaleState()
            yield None

        self.stop()

    def hearthRendState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        self.stop()
        self.anim = 'rend'
        r = rendRange[self.direction]

        if self.stats.mp < 10 or not self.stats.rend:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 10

        # charge
        # TODO: sound/particle effect here
        while self._animator.index == 0:
            yield None

        fire = ika.Entity(self.x, self.y, self.layer, 'rend.ika-sprite')
        f = self.direction * 5 # hack.

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.hearthRend.Play()

        while not self._animator.kill:
            ents = self.detectCollision(r[self._animator.index] + (self.layer,))
            fire.specframe = f + self._animator.index

            for e in ents:
                if isinstance(e, Enemy) and not e.invincible and e not in hitList:
                    hitList.append(e)
                    e.hurt(int(self.stats.att + self.stats.mag) * 2, 300, self.direction)
                elif isinstance(e, IceWall):
                    # TODO: some sort of nice animation.
                    setattr(savedata, e.flagName, 'Broken')

                    system.engineObj.destroyEntity(e)
                    system.engineObj.things.append(Caption('~1The ice melted!'))

            yield None

        del fire

        # stall period:
        for i in range(30):
            yield None

    def crushingGaleState(self):
        class Saver(object):
            def __init__(_self):
                _self.speed = self.speed
                _self.o = self.ent.entobs
                _self.i = self.invincible
                _self.l = system.engineObj.camera.locked
            def __del__(_self):
                self.speed = _self.speed
                self.ent.entobs = _self.o
                self.invincible = _self.i
                system.engineObj.camera.locked = _self.l

        saver = Saver()

        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        self.stop()
        self.anim = 'stand'

        if self.stats.mp < 15 or not self.stats.gale:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 15

        camera = system.engineObj.camera

        camera.locked = True
        dx, dy = dir.delta[self.direction]

        # charge

        sound.crushingGale.Play()

        for i in range(30):
            ika.Map.xwin += dx * 2
            ika.Map.ywin += dy * 2
            yield None

        self.invincible = True
        self.ent.entobs = False

        self.anim = 'thrust'
        r = galeRange[self.direction] + (self.layer,)
        self.move(self.direction, 100000)
        self.speed *= 10
        camera.locked = False
        for i in range(60):
            ents = self.detectCollision(r)
            for e in ents:
                if isinstance(e, Enemy) and not e.invincible:
                    e.hurt(self.stats.att + self.stats.mag * 2, 300, (self.direction + 2) & 3)

            yield None
            self.speed = max(saver.speed, self.speed - 20)

        while True:
            ents = [x for x in self.detectCollision((0, 0, self.ent.hotwidth, self.ent.hotheight, self.layer)) if isinstance(x, Gap)]
            if not ents:
                break
            else:
                yield None

        self.stop()

        # stall
        for i in range(20):
            yield None

    def healingRainState(self):

        self.stop()

        self.anim = 'magic'

        if self.stats.mp < 20 or not self.stats.heal:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 20

        # not much to do here :)
        # TODO: particles or something, for confirmation for the player
        # if for no other reason.

        sound.healingRain.Play()

        self.invincible = True

        for i in range(20):
            yield None

        amount = self.stats.mag * 2 + 25
        amount += int(amount * ika.Random(-10, 10) * 0.01)
        self.stats.hp += min(20, amount)

        ents = self.detectCollision((-16, -16, 32, 32, self.layer))

        for e in ents:
            if isinstance(e, IceChunks):
                e.freeze()
                system.engineObj.things.append(Caption('~1The ice froze over!'))
                system.engineObj.destroyEntity(e)
                break

        for i in range(45):
            yield None

        self.invincible = False

    def smokeScreenState(self):
        pass

    def shiverState(self):
        self.stop()
        self.anim = 'thrust'

        if self.stats.mp < 45 or not self.stats.shiver:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 45

        ents = self.detectCollision((
            self.x-160, self.y-160, 320, 320, self.layer
            ))

        for e in ents:
            if isinstance(e, Enemy) and not e.invincible:
                d = dir.fromDelta(self.x - e.x, self.y - e.y)
                e.hurt((self.stats.att + self.stats.mag) * 3, 400, d)

        self.stop()

        # stall
        for i in range(100):
            yield None

    def vivifyState(self):
        pass

    def ternionState(self):
        pass

    def dieTask(self):
        self.state = self.deathState()
        self._state()
        self.anim = 'die'
        raise GameOverException()
        if False:
            yield None

    def deathState(self):
        self.invincible = True
        s = self.hurtState(300, dir.invert[self.direction])
        yield next(s)
        self.anim = 'die'
        for x in s:
            yield None

        while True:
            yield None

    def giveMPforHit(self):
        self.stats.mp += ika.Random(0,2 + self.stats.level//10)
