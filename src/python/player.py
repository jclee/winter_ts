from browser import window
import ika

import sound

from gameover import GameLoseException

from entity import OldEntity
from enemy import OldEnemy
from obstacle import IceWall, IceChunks, Gap


PLAYER_SPRITE = 'protagonist.ika-sprite'

# one entry for each direction
_playerAnim = {
    'walk' : ((
        window.animator.makeAnimRange(28, 36, 8),
        window.animator.makeAnimRange(19, 27, 8),
        window.animator.makeAnimRange(10, 18, 8),
        window.animator.makeAnimRange(1, 9, 8),
        window.animator.makeAnimRange(28, 36, 8),
        window.animator.makeAnimRange(19, 27, 8),
        window.animator.makeAnimRange(28, 36, 8),
        window.animator.makeAnimRange(19, 27, 8),
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

class OldPlayer(OldEntity):
    def __init__(self, engineRef, x=0, y=0, layer=0):
        OldEntity.__init__(self, engineRef, engineRef.map.addSprite(x, y, layer, PLAYER_SPRITE), _playerAnim)
        self.setState(self.standState())

        self.stats.maxhp = 80
        self.stats.maxmp = 40
        self.stats.att = 5
        self.stats.mag = 1
        self.stats.pres = 1
        self.stats.mres = 1
        self.stats.level = 1
        self.stats.exp = 0
        self.stats.next = 10

        self.stats.hp = 80
        self.stats.mp = 40

    def isKind(self, kind):
        return kind == 'Player' or super(OldPlayer, self).isKind(kind)

    def giveXP(self, amount):
        self.stats.exp += amount
        if self.stats.exp >= self.stats.next:
            self.levelUp()

    def levelUp(self):

        sound.achievement.Play()

        while self.stats.exp >= self.stats.next:
            self.stats.maxhp += window.random(2, 7)
            self.stats.maxmp += window.random(2, 6)

            statlist = []
            for n in range(3):
                if not statlist:
                    statlist = ['att', 'mag', 'pres', 'mres']
                s = statlist[window.random(0,len(statlist))]
                self.stats[s]+= 1
                statlist.remove(s)

            self.stats.level += 1

            self.stats.maxhp = min(self.stats.maxhp, 285)
            self.stats.maxmp = min(self.stats.maxmp, 285)
            self.stats.exp -= self.stats.next
            self.stats.next = self.stats.level * (self.stats.level + 1) * 5

        self.engineRef.things.append(window.caption.Caption.new(self.engineRef, self.engineRef.font, 'Level %i!' % self.stats.level))

    def defaultState(self):
        return self.standState()

    def standState(self):
        self.stop()
        self.startAnimation('stand')
        while True:
            if self.engineRef.controls.attack():
                self.setState(self.slashState())
            elif self.engineRef.controls.rend():
                self.setState(self.hearthRendState())
                yield None
            elif self.engineRef.controls.gale():
                self.setState(self.crushingGaleState())
                yield None
            elif self.engineRef.controls.heal():
                self.setState(self.healingRainState())
                yield None
            elif self.engineRef.controls.shiver():
                self.setState(self.shiverState())
                yield None
            elif self.engineRef.controls.left() or self.engineRef.controls.right() or self.engineRef.controls.up() or self.engineRef.controls.down():
                self.setState(self.walkState())
                next(self._state) # get the walk state started right now.
            yield None

    def walkState(self):
        oldDir = self.direction
        self.startAnimation('walk')

        while True:

            if self.engineRef.controls.attack():
                self.setState(self.slashState())
                yield None
            elif self.engineRef.controls.rend():
                self.setState(self.hearthRendState())
                yield None
            elif self.engineRef.controls.gale():
                self.setState(self.crushingGaleState())
                yield None
            elif self.engineRef.controls.heal():
                self.setState(self.healingRainState())
                yield None
            elif self.engineRef.controls.shiver():
                self.setState(self.shiverState())
                yield None
            elif self.engineRef.controls.left():
                if self.engineRef.controls.up():
                    d = self.engineRef.dir.UpLeft
                elif self.engineRef.controls.down():
                    d = self.engineRef.dir.DownLeft
                else:
                    d = self.engineRef.dir.Left
            elif self.engineRef.controls.right():
                if self.engineRef.controls.up():
                    d = self.engineRef.dir.UpRight
                elif self.engineRef.controls.down():
                    d = self.engineRef.dir.DownRight
                else:
                    d = self.engineRef.dir.Right
            elif self.engineRef.controls.up():
                d = self.engineRef.dir.Up
            elif self.engineRef.controls.down():
                d = self.engineRef.dir.Down
            else:
                self.setState(self.standState())
                yield None

            self.move(d)

            # handle animation and junk
            if d != oldDir:
                self.startAnimation('walk')
                self.direction = d
                oldDir = d
            yield None

    def slashState(self):
        self.stop()
        self.startAnimation('slash')
        r = slashRange[self.direction]
        backslash = False
        backthrust = False

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash1.Play()

        while self.isAnimating():
            rect = list(r[self.getAnimationIndex()]) + [self.sprite.layer]
            rect[0] += self.sprite.x
            rect[1] += self.sprite.y
            ents = self.engineRef.map.spritesAt(*rect)
            for e in ents:
                x = self.engineRef.nameToEntityMap[e.name]
                if x.isKind('Enemy') and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(self.stats.att, 120, self.direction)
                    self.giveMPforHit()

            if self.engineRef.controls.up() and self.direction == self.engineRef.dir.Down:  backthrust = True
            elif self.engineRef.controls.down() and self.direction == self.engineRef.dir.Up:  backthrust = True
            elif self.engineRef.controls.left() and self.direction in [self.engineRef.dir.Right, self.engineRef.dir.UpRight, self.engineRef.dir.DownRight]:  backthrust = True
            elif self.engineRef.controls.right() and self.direction in [self.engineRef.dir.Left, self.engineRef.dir.UpLeft, self.engineRef.dir.DownLeft]:  backthrust = True

            elif self.engineRef.controls.attack():
                backslash = True

            yield None

        if backthrust:
            self.setState(self.backThrustState())
            yield None
        elif backslash:
            self.setState(self.backSlashState())
            yield None
        else:
            # Stall:
            count = 10
            while count > 0:
                count -= 1
                if self.engineRef.controls.attack():
                    self.setState(self.thrustState())
                yield None

    def backSlashState(self):
        self.stop()
        self.startAnimation('backslash')
        r = backSlashRange[self.direction]

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash2.Play()

        while self.isAnimating():
            rect = list(r[self.getAnimationIndex()]) + [self.sprite.layer]
            rect[0] += self.sprite.x
            rect[1] += self.sprite.y
            ents = self.engineRef.map.spritesAt(*rect)
            for e in ents:
                x = self.engineRef.nameToEntityMap[e.name]
                if x.isKind('Enemy') and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(self.stats.att, 130, self.direction)
                    self.giveMPforHit()

            yield None

        # Stall:
        count = 10
        while count > 0:
            count -= 1
            if self.engineRef.controls.rend():
                self.setState(self.hearthRendState())
            elif self.engineRef.controls.attack():
                self.setState(self.thrustState())
            yield None

    def thrustState(self):
        if self.direction == self.engineRef.dir.UpLeft or self.direction == self.engineRef.dir.DownLeft:
            self.direction = self.engineRef.dir.Left
        elif self.direction == self.engineRef.dir.UpRight or self.direction == self.engineRef.dir.DownRight:
            self.direction = self.engineRef.dir.Right

        oldSpeed = self.sprite.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.sprite.speed = oldSpeed
        self._onStateExit = restoreVars

        self.startAnimation('thrust')
        self.sprite.speed += 800
        self.move(self.direction, 1000)

        r = thrustRange[self.direction] + (self.sprite.layer,)
        rect = list(r)

        sound.slash3.Play()

        # hack since I need to break out of two levels at once
        def thing():
            i = 8
            while i > 0:
                i -= 1
                self.sprite.speed -= (12 - i) * 10

                rect[0] = r[0] + self.sprite.x
                rect[1] = r[1] + self.sprite.y
                ents = self.engineRef.map.spritesAt(*rect)
                for e in ents:
                    x = self.engineRef.nameToEntityMap[e.name]
                    if x.isKind('Enemy') and not x.invincible:
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
            self.sprite.speed = max(10, self.sprite.speed - 10)
            yield None

        self.stop()

    def backThrustState(self):
        if self.direction == self.engineRef.dir.UpLeft or self.direction == self.engineRef.dir.DownLeft:
            self.direction = self.engineRef.dir.Left
        elif self.direction == self.engineRef.dir.UpRight or self.direction == self.engineRef.dir.DownRight:
            self.direction = self.engineRef.dir.Right

        oldSpeed = self.sprite.speed
        def restoreVars(self=self, oldSpeed=oldSpeed):
            self.sprite.speed = oldSpeed
        self._onStateExit = restoreVars

        self.startAnimation('backthrust')
        self.sprite.speed += 400
        self.move(self.engineRef.dir.invert(self.direction), 1000)

        i = 8
        while i > 0:
            i -= 1
            self.sprite.speed -= 40
            yield None

        i = 30
        thrust = False
        gale = False

        while i > 0:
            i -= 1
            self.sprite.speed = max(0, self.sprite.speed - 10)
            if self.engineRef.controls.attack():
                thrust = True
            elif self.engineRef.controls.gale():
                gale = True
            yield None

        self.direction = self.engineRef.dir.invert(self.direction)

        if thrust:
            self.setState(self.thrustState())
            yield None

        elif gale:
            self.setState(self.crushingGaleState())
            yield None

        self.stop()

    def hearthRendState(self):
        if self.direction == self.engineRef.dir.UpLeft or self.direction == self.engineRef.dir.DownLeft:
            self.direction = self.engineRef.dir.Left
        elif self.direction == self.engineRef.dir.UpRight or self.direction == self.engineRef.dir.DownRight:
            self.direction = self.engineRef.dir.Right

        self.stop()
        self.startAnimation('rend')
        r = rendRange[self.direction]

        if self.stats.mp < 10 or 'firerune' not in self.engineRef.saveFlags:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 10

        # charge
        # TODO: sound/particle effect here
        for i in range(12):
            yield None

        fire = self.engineRef.map.addSprite(self.sprite.x, self.sprite.y, self.sprite.layer, 'rend.ika-sprite')
        f = self.direction * 5 # hack.

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.hearthRend.Play()

        while self.isAnimating():
            ents = self.detectCollision(r[self.getAnimationIndex()] + (self.sprite.layer,))
            fire.specframe = f + self.getAnimationIndex()

            for e in ents:
                if e.isKind('Enemy') and not e.invincible and e not in hitList:
                    hitList.append(e)
                    e.hurt(int(self.stats.att + self.stats.mag) * 2, 300, self.direction)
                elif e.isKind('IceWall'):
                    # TODO: some sort of nice animation.
                    self.engineRef.saveFlags[e.flagName] = 'Broken'

                    self.engineRef.destroyEntity(e)
                    self.engineRef.things.append(window.caption.Caption.new(self.engineRef, self.engineRef.font, '~1The ice melted!'))

            yield None

        self.engineRef.map.removeSprite(fire)

        # stall period:
        for i in range(30):
            yield None

    def crushingGaleState(self):
        oldSpeed = self.sprite.speed
        oldObs = self.sprite.entobs
        oldInvincible = self.invincible
        oldCameraLocked = self.engineRef.camera.locked
        def restoreVars(self=self, oldSpeed=oldSpeed, oldObs=oldObs, oldInvincible=oldInvincible, oldCameraLocked=oldCameraLocked):
            self.sprite.speed = oldSpeed
            self.sprite.entobs = oldObs
            self.invincible = oldInvincible
            self.engineRef.camera.locked = oldCameraLocked
        self._onStateExit = restoreVars

        if self.direction == self.engineRef.dir.UpLeft or self.direction == self.engineRef.dir.DownLeft:
            self.direction = self.engineRef.dir.Left
        elif self.direction == self.engineRef.dir.UpRight or self.direction == self.engineRef.dir.DownRight:
            self.direction = self.engineRef.dir.Right

        self.stop()
        self.startAnimation('stand')

        if self.stats.mp < 15 or 'windrune' not in self.engineRef.saveFlags:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 15

        camera = self.engineRef.camera

        camera.locked = True
        delta = self.engineRef.dir.toDelta(self.direction)

        # charge

        sound.crushingGale.Play()

        for i in range(30):
            self.engineRef.map.xwin += delta.x * 2
            self.engineRef.map.ywin += delta.y * 2
            yield None

        self.invincible = True
        self.sprite.entobs = False

        self.startAnimation('thrust')
        r = galeRange[self.direction] + (self.sprite.layer,)
        self.move(self.direction, 100000)
        self.sprite.speed *= 10
        camera.locked = False
        for i in range(60):
            ents = self.detectCollision(r)
            for e in ents:
                if e.isKind('Enemy') and not e.invincible:
                    e.hurt(self.stats.att + self.stats.mag * 2, 300, (self.direction + 2) & 3)

            yield None
            self.sprite.speed = max(oldSpeed, self.sprite.speed - 20)

        while True:
            ents = [x for x in self.detectCollision((0, 0, self.sprite.hotwidth, self.sprite.hotheight, self.sprite.layer)) if x.isKind('Gap')]
            if not ents:
                break
            else:
                yield None

        self.stop()

        # stall
        for i in range(20):
            yield None

    def healingRainState(self):
        oldInvincible = self.invincible
        def restoreVars(self=self, oldInvincible=oldInvincible):
            self.invincible = oldInvincible
        self._onStateExit = restoreVars

        self.stop()

        self.startAnimation('magic')

        if self.stats.mp < 20 or 'waterrune' not in self.engineRef.saveFlags:
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
        amount += int(amount * window.random(-10, 10) * 0.01)
        self.stats.hp += min(20, amount)

        ents = self.detectCollision((-16, -16, 32, 32, self.sprite.layer))

        for e in ents:
            if e.isKind('IceChunks'):
                e.freeze()
                self.engineRef.things.append(window.caption.Caption.new(self.engineRef, self.engineRef.font, '~1The ice froze over!'))
                self.engineRef.destroyEntity(e)
                break

        for i in range(45):
            yield None

    def shiverState(self):
        self.stop()
        self.startAnimation('thrust')

        if self.stats.mp < 45 or 'cowardrune' not in self.engineRef.saveFlags:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 45

        ents = self.detectCollision((
            self.sprite.x-160, self.sprite.y-160, 320, 320, self.sprite.layer
            ))

        for e in ents:
            if e.isKind('Enemy') and not e.invincible:
                d = self.engineRef.dir.fromDelta(self.sprite.x - e.sprite.x, self.sprite.y - e.sprite.y)
                e.hurt((self.stats.att + self.stats.mag) * 3, 400, d)

        self.stop()

        # stall
        for i in range(100):
            yield None

    def die(self):
        self.setState(self.deathState())
        raise GameLoseException()

    def deathState(self):
        self.invincible = True
        s = self.hurtState(300, self.engineRef.dir.invert(self.direction))
        yield next(s)
        self.startAnimation('die')
        for x in s:
            yield None

        while True:
            yield None

    def noOpState(self):
        while True:
            yield None

    def giveMPforHit(self):
        self.stats.mp += window.random(0,2 + self.stats.level//10)
