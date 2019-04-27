import { makeAnimRange } from "./animator.js"
import { Caption } from "./caption.js"
import { Direction, fromDelta, invert, toDelta } from "./Direction.js"
import { Entity } from "./entity.js"
import { IceChunks, IceWall } from "./obstacle.js"
import { PyEngine, random } from "./winter.js"

export const PLAYER_SPRITE = 'protagonist.ika-sprite'

// one entry for each direction
const _playerAnim: {[key: string]: [[number, number][][], boolean]} = {
    walk: [[
        makeAnimRange(28, 36, 8),
        makeAnimRange(19, 27, 8),
        makeAnimRange(10, 18, 8),
        makeAnimRange(1, 9, 8),
        makeAnimRange(28, 36, 8),
        makeAnimRange(19, 27, 8),
        makeAnimRange(28, 36, 8),
        makeAnimRange(19, 27, 8),
    ], true],

    slash: [[
        [[63, 8], [64, 6], [65, 4], [66, 2], [67, 8]],
        [[54, 8], [55, 6], [56, 4], [57, 2], [58, 8]],
        [[45, 8], [46, 6], [47, 4], [48, 2], [49, 8]],
        [[36, 8], [37, 6], [38, 4], [39, 2], [40, 8]],
        [[63, 8], [64, 6], [65, 4], [66, 2], [67, 8]],
        [[54, 8], [55, 6], [56, 4], [57, 2], [58, 8]],
        [[63, 8], [64, 6], [65, 4], [66, 2], [67, 8]],
        [[54, 8], [55, 6], [56, 4], [57, 2], [58, 8]],
    ], false],

    backslash: [[
        [[67, 8], [66, 6], [65, 4], [64, 2], [63, 8]],
        [[58, 8], [57, 6], [56, 4], [55, 2], [54, 8]],
        [[49, 8], [48, 6], [47, 4], [46, 2], [45, 8]],
        [[40, 8], [39, 6], [38, 4], [37, 2], [36, 8]],
        [[67, 8], [66, 6], [65, 4], [64, 2], [63, 8]],
        [[58, 8], [57, 6], [56, 4], [55, 2], [54, 8]],
        [[67, 8], [66, 6], [65, 4], [64, 2], [63, 8]],
        [[58, 8], [57, 6], [56, 4], [55, 2], [54, 8]],
    ], false],

    thrust: [[
        [[67, 6], [66, 4], [65, 1000]],
        [[58, 6], [57, 4], [56, 1000]],
        [[49, 6], [48, 4], [47, 1000]],
        [[40, 6], [39, 4], [38, 1000]],
        [[67, 6], [66, 4], [65, 1000]],
        [[58, 6], [57, 4], [56, 1000]],
        [[67, 6], [66, 4], [65, 1000]],
        [[58, 6], [57, 4], [56, 1000]],
    ], false],

    backthrust: [[
        //[[90, 1000]],
        [[99, 1000]],
        [[90, 1000]],
        //[[72, 1000]],
        [[81, 1000]],
        [[72, 1000]],
        [[99, 1000]],
        [[90, 1000]],
        [[99, 1000]],
        [[90, 1000]],
    ], true],

    rend: [[
        [[63, 12], [64, 8], [65, 6], [66, 2], [67, 12]],
        [[54, 12], [55, 8], [56, 6], [57, 2], [58, 12]],
        [[45, 12], [46, 8], [47, 6], [48, 2], [49, 12]],
        [[36, 12], [37, 8], [38, 6], [39, 2], [40, 12]],
        [[63, 12], [64, 8], [65, 6], [66, 2], [67, 12]],
        [[54, 12], [55, 8], [56, 6], [57, 2], [58, 12]],
        [[63, 12], [64, 8], [65, 6], [66, 2], [67, 12]],
        [[54, 12], [55, 8], [56, 6], [57, 2], [58, 12]],
    ], false],

    stand: [[
        [[27, 1000]],
        [[18, 1000]],
        [[9, 1000]],
        [[0, 1000]],
        [[27, 1000]],
        [[18, 1000]],
        [[27, 1000]],
        [[18, 1000]],
    ], true],

    hurt: [[
        [[90, 1000]],
        [[99, 1000]],
        [[72, 1000]],
        [[81, 1000]],
        [[90, 1000]],
        [[99, 1000]],
        [[90, 1000]],
        [[99, 1000]],
    ], true],

    die: [[
            [[90, 20], [91, 20], [92, 1000]],
            [[99, 20], [100, 20], [101, 1000]],
            [[72, 20], [73, 20], [74, 1000]],
            [[81, 20], [82, 20], [83, 1000]],
            [[90, 20], [91, 20], [92, 1000]],
            [[99, 20], [100, 20], [101, 1000]],
            [[90, 20], [91, 20], [92, 1000]],
            [[99, 20], [100, 20], [101, 1000]],
    ], false],

    // temporary:  copy the normal standing frames.
    magic: [[
        [[27, 1000]],
        [[18, 1000]],
        [[9, 1000]],
        [[0, 1000]],
        [[27, 1000]],
        [[18, 1000]],
        [[27, 1000]],
        [[18, 1000]]
    ], true],
}

const thrustRange: [number, number, number, number][] = [
    [-22,  -2, 16, 8],
    [ 15,  -2, 16, 8],
    [  6, -27, 10, 27],
    [  6,  17, 10, 12],
    [-22,  -2, 16, 8],
    [ 15,  -2, 16, 8],
    [-22,  -2, 16, 8],
    [ 15,  -2, 16, 8],
]

const slashRange: [number, number, number, number][][] = [
    [[-18, -14, 12,  8], [-20,  -8, 14,  8], [-22,  -2, 16,  8], [-20,   4, 14,  8], [-18,  10, 12,  8]],
    [[ 15, -14, 12,  8], [ 15,  -8, 14,  8], [ 15,  -2, 16,  8], [ 15,   4, 14,  8], [ 15,  10, 12,  8]],
    [[-14, -27, 10, 27], [ -4, -27, 10, 27], [  6, -27, 10, 27], [ 16, -27, 10, 27], [ 16, -27, 10, 27]],
    [[ 16,  17, 10, 12], [ 16,  17, 10, 12], [  6,  17, 10, 12], [ -4,  17, 10, 12], [-14,  17, 10, 12]],
    [[-18, -14, 12,  8], [-20,  -8, 14,  8], [-22,  -2, 16,  8], [-20,   4, 14,  8], [-18,  10, 12,  8]],
    [[ 15, -14, 12,  8], [ 15,  -8, 14,  8], [ 15,  -2, 16,  8], [ 15,   4, 14,  8], [ 15,  10, 12,  8]],
    [[-18, -14, 12,  8], [-20,  -8, 14,  8], [-22,  -2, 16,  8], [-20,   4, 14,  8], [-18,  10, 12,  8]],
    [[ 15, -14, 12,  8], [ 15,  -8, 14,  8], [ 15,  -2, 16,  8], [ 15,   4, 14,  8], [ 15,  10, 12,  8]],
]

const rendRange: [number, number, number, number][][] = [
    [[-22, -14, 16,  8], [-24,  -8, 18,  8], [-26,  -2, 20,  8], [-24,   4, 18,  8], [-22,  10, 16,  8]],
    [[ 15, -14, 16,  8], [ 15,  -8, 18,  8], [ 15,  -2, 20,  8], [ 15,   4, 18,  8], [ 15,  10, 16,  8]],

    [[-14, -29, 10, 29], [ -4, -29, 10, 29], [  6, -29, 10, 29], [ 16, -29, 10, 29], [ 16, -29, 10, 29]],
    [[ 16,  17, 10, 16], [ 16,  17, 10, 16], [  6,  17, 10, 16], [ -4,  17, 10, 16], [-14,  17, 10, 16]],

    [[-22, -14, 16,  8], [-24,  -8, 18,  8], [-26,  -2, 20,  8], [-24,   4, 18,  8], [-22,  10, 16,  8]],
    [[ 15, -14, 16,  8], [ 15,  -8, 18,  8], [ 15,  -2, 20,  8], [ 15,   4, 18,  8], [ 15,  10, 16,  8]],

    [[-22, -14, 16,  8], [-24,  -8, 18,  8], [-26,  -2, 20,  8], [-24,   4, 18,  8], [-22,  10, 16,  8]],
    [[ 15, -14, 16,  8], [ 15,  -8, 18,  8], [ 15,  -2, 20,  8], [ 15,   4, 18,  8], [ 15,  10, 16,  8]],
]

const galeRange: [number, number, number, number][] = [
    [-17, -8, 8, 24],
    [15, -8, 8, 24],
    [-8, -8, 24, 8],
    [-8, 16, 24, 8],
    [-17, -8, 8, 24],
    [15, -8, 8, 24],
    [-17, -8, 8, 24],
    [15, -8, 8, 24],
]

function reversed(x: [number, number, number, number][]): [number, number, number, number][] {
    return x.slice(0).reverse()
}
const backSlashRange: [number, number, number, number][][] = slashRange.map(x => reversed(x))

export class Player extends Entity {
    constructor(
        engineRef: PyEngine,
        x: number = 0,
        y: number = 0,
        layer: number = 0
    ) {
        const engine = engineRef.getEngine()
        const sprite = engine.map.addSprite(x, y, layer, PLAYER_SPRITE)
        super(engineRef, sprite, _playerAnim)
        this.setState(this.standState())

        this.stats.maxhp = 80
        this.stats.maxmp = 40
        this.stats.att = 5
        this.stats.mag = 1
        this.stats.pres = 1
        this.stats.mres = 1
        this.stats.level = 1
        this.stats.exp = 0
        this.stats.next = 10

        this.stats.hp = 80
        this.stats.mp = 40
    }

    isKind(kind: string) {
        return kind === 'Player' || super.isKind(kind)
    }

    giveXP(amount: number) {
        this.stats.exp += amount
        if (this.stats.exp >= this.stats.next) {
            this.levelUp()
        }
    }

    levelUp() {
        this.engine.sounds.achievement.play()

        while (this.stats.exp >= this.stats.next) {
            this.stats.maxhp += random(2, 7)
            this.stats.maxmp += random(2, 6)

            let statlist: string[] = []
            for (let n = 0; n < 3; ++ n) {
                if (statlist.length === 0) {
                    statlist = ['att', 'mag', 'pres', 'mres']
                }
                const s = statlist[random(0, statlist.length)]
                if (s === 'att') {
                    this.stats.att += 1
                } else if (s === 'mag') {
                    this.stats.mag += 1
                } else if (s === 'pres') {
                    this.stats.pres += 1
                } else if (s === 'mres') {
                    this.stats.mres += 1
                }
                statlist = statlist.filter(x => x !== s)
            }

            this.stats.level += 1

            this.stats.maxhp = Math.min(this.stats.maxhp, 285)
            this.stats.maxmp = Math.min(this.stats.maxmp, 285)
            this.stats.exp -= this.stats.next
            this.stats.next = this.stats.level * (this.stats.level + 1) * 5
        }

        this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font, `Level ${this.stats.level}!`))
    }

    defaultState() {
        return this.standState()
    }

    *standState() {
        this.stop()
        this.startAnimation('stand')
        while (true) {
            if (this.engine.controls.attack()) {
                this.setState(this.slashState())
            } else if (this.engine.controls.rend()) {
                this.setState(this.hearthRendState())
                yield null
            } else if (this.engine.controls.gale()) {
                this.setState(this.crushingGaleState())
                yield null
            } else if (this.engine.controls.heal()) {
                this.setState(this.healingRainState())
                yield null
            } else if (this.engine.controls.shiver()) {
                this.setState(this.shiverState())
                yield null
            } else if (this.engine.controls.left() || this.engine.controls.right() || this.engine.controls.up() || this.engine.controls.down()) {
                this.setState(this.walkState())
                if (this._state === null) {
                    throw new Error("Unexpected null state")
                }
                this._state.next() // get the walk state started right now.
            }
            yield null
        }
    }

    *walkState() {
        let oldDir = this.direction
        this.startAnimation('walk')

        while (true) {
            let d: Direction

            if (this.engine.controls.attack()) {
                this.setState(this.slashState())
                yield null
                return
            } else if (this.engine.controls.rend()) {
                this.setState(this.hearthRendState())
                yield null
                return
            } else if (this.engine.controls.gale()) {
                this.setState(this.crushingGaleState())
                yield null
                return
            } else if (this.engine.controls.heal()) {
                this.setState(this.healingRainState())
                yield null
                return
            } else if (this.engine.controls.shiver()) {
                this.setState(this.shiverState())
                yield null
                return
            } else if (this.engine.controls.left()) {
                if (this.engine.controls.up()) {
                    d = Direction.UpLeft
                } else if (this.engine.controls.down()) {
                    d = Direction.DownLeft
                } else {
                    d = Direction.Left
                }
            } else if (this.engine.controls.right()) {
                if (this.engine.controls.up()) {
                    d = Direction.UpRight
                } else if (this.engine.controls.down()) {
                    d = Direction.DownRight
                } else {
                    d = Direction.Right
                }
            } else if (this.engine.controls.up()) {
                d = Direction.Up
            } else if (this.engine.controls.down()) {
                d = Direction.Down
            } else {
                this.setState(this.standState())
                yield null
                return
            }

            this.move(d)

            // handle animation and junk
            if (d !== oldDir) {
                this.startAnimation('walk')
                this.direction = d
                oldDir = d
            }
            yield null
        }
    }

    *slashState() {
        this.stop()
        this.startAnimation('slash')
        const r = slashRange[this.direction]
        let backslash = false
        let backthrust = false

        // when we hit an entity, we append it here so that
        // we know not to hurt it again.
        const hitList: Entity[] = []

        this.engine.sounds.slash1.play()

        while (this.isAnimating()) {
            const ents = this.detectCollision(r[this.getAnimationIndex()])
            for (let e of ents) {
                if (e.isKind('Enemy') && !e.invincible && !hitList.includes(e)) {
                    hitList.push(e)
                    e.hurt(this.stats.att, 120, this.direction)
                    this.giveMPforHit()
                }
            }

            if (this.engine.controls.up() && this.direction === Direction.Down) {
                backthrust = true
            } else if (this.engine.controls.down() && this.direction === Direction.Up) {
                backthrust = true
            } else if (this.engine.controls.left() && (
                    this.direction === Direction.Right
                    || this.direction === Direction.UpRight
                    || this.direction === Direction.DownRight)) {
                backthrust = true
            } else if (this.engine.controls.right() && (
                    this.direction === Direction.Left
                    || this.direction === Direction.UpLeft
                    || this.direction === Direction.DownLeft)) {
                backthrust = true
            } else if (this.engine.controls.attack()) {
                backslash = true
            }

            yield null
        }

        if (backthrust) {
            this.setState(this.backThrustState())
            yield null
        } else if (backslash) {
            this.setState(this.backSlashState())
            yield null
        } else {
            // Stall:
            let count = 10
            while (count > 0) {
                count -= 1
                if (this.engine.controls.attack()) {
                    this.setState(this.thrustState())
                }
                yield null
            }
        }
    }

    *backSlashState() {
        this.stop()
        this.startAnimation('backslash')
        const r = backSlashRange[this.direction]

        // when we hit an entity, we append it here so that
        // we know not to hurt it again.
        const hitList: Entity[] = []

        this.engine.sounds.slash2.play()

        while (this.isAnimating()) {
            const ents = this.detectCollision(r[this.getAnimationIndex()])
            for (let e of ents) {
                if (e.isKind('Enemy') && !e.invincible && !hitList.includes(e)) {
                    hitList.push(e)
                    e.hurt(this.stats.att, 130, this.direction)
                    this.giveMPforHit()
                }
            }

            yield null
        }

        // Stall:
        let count = 10
        while (count > 0) {
            count -= 1
            if (this.engine.controls.rend()) {
                this.setState(this.hearthRendState())
            } else if (this.engine.controls.attack()) {
                this.setState(this.thrustState())
            }
            yield null
        }
    }

    *thrustState() {
        if (this.direction === Direction.UpLeft || this.direction === Direction.DownLeft) {
            this.direction = Direction.Left
        } else if (this.direction === Direction.UpRight || this.direction === Direction.DownRight) {
            this.direction = Direction.Right
        }

        const oldSpeed = this.sprite.speed
        this._onStateExit = () => {
            this.sprite.speed = oldSpeed
        }

        this.startAnimation('thrust')
        this.sprite.speed += 800
        this.move(this.direction, 1000)

        const r = thrustRange[this.direction]

        this.engine.sounds.slash3.play()

        outerLoop: for (let i = 8; i > 0; --i) {
            this.sprite.speed -= (12 - i) * 10

            const ents = this.detectCollision(r)
            for (let e of ents) {
                if (e.isKind('Enemy') && !e.invincible) {
                    e.hurt(Math.floor(this.stats.att * 1.5), 300, this.direction)
                    this.giveMPforHit()
                    this.stop()
                    break outerLoop
                }
            }
            yield null
        }

        for (let i = 0; i < 30; ++i) {
            this.sprite.speed = Math.max(10, this.sprite.speed - 10)
            yield null
        }

        this.stop()
    }

    *backThrustState() {
        if (this.direction === Direction.UpLeft || this.direction === Direction.DownLeft) {
            this.direction = Direction.Left
        } else if (this.direction === Direction.UpRight || this.direction === Direction.DownRight) {
            this.direction = Direction.Right
        }

        const oldSpeed = this.sprite.speed
        this._onStateExit = () => {
            this.sprite.speed = oldSpeed
        }

        this.startAnimation('backthrust')
        this.sprite.speed += 400
        this.move(invert(this.direction), 1000)

        for (let i = 0; i < 8; ++i) {
            this.sprite.speed -= 40
            yield null
        }

        let thrust = false
        let gale = false

        for (let i = 0; i < 30; ++i) {
            this.sprite.speed = Math.max(0, this.sprite.speed - 10)
            if (this.engine.controls.attack()) {
                thrust = true
            } else if (this.engine.controls.gale()) {
                gale = true
            }
            yield null
        }

        this.direction = invert(this.direction)

        if (thrust) {
            this.setState(this.thrustState())
            yield null
        } else if (gale) {
            this.setState(this.crushingGaleState())
            yield null
        }

        this.stop()
    }

    *hearthRendState() {
        if (this.direction === Direction.UpLeft || this.direction === Direction.DownLeft) {
            this.direction = Direction.Left
        } else if (this.direction === Direction.UpRight || this.direction === Direction.DownRight) {
            this.direction = Direction.Right
        }

        this.stop()
        this.startAnimation('rend')
        const r = rendRange[this.direction]

        if (this.stats.mp < 10 || !this.engineRef.hasSaveFlag('firerune')) {
            this.engine.sounds.menuBuzz.play()
            return
        }

        this.stats.mp -= 10

        // charge
        // TODO: sound/particle effect here
        for (let i = 0; i < 12; ++i) {
            yield null
        }

        const fire = this.engine.map.addSprite(this.sprite.x, this.sprite.y, this.sprite.layer, 'rend.ika-sprite')
        const f = this.direction * 5 // hack.

        // when we hit an entity, we append it here so that
        // we know not to hurt it again.
        let hitList: Entity[] = []

        this.engine.sounds.hearthRend.play()

        while (this.isAnimating()) {
            const ents = this.detectCollision(r[this.getAnimationIndex()])
            fire.specframe = f + this.getAnimationIndex()

            for (let e of ents) {
                if (e.isKind('Enemy') && !e.invincible && !hitList.includes(e)) {
                    hitList.push(e)
                    e.hurt(Math.floor(this.stats.att + this.stats.mag) * 2, 300, this.direction)
                } else if (e.isKind('IceWall')) {
                    // TODO: some sort of nice animation.
                    this.engineRef.setSaveFlag((e as IceWall).flagName as string, 'Broken')

                    this.engineRef.destroyEntity(e)
                    this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font, '~1The ice melted!'))
                }
            }

            yield null
        }

        this.engine.map.removeSprite(fire)

        // stall period:
        for (let i = 0; i < 30; ++i) {
            yield null
        }
    }

    *crushingGaleState() {
        const oldSpeed = this.sprite.speed
        const oldObs = this.sprite.entobs
        const oldInvincible = this.invincible
        const oldCameraLocked = this.engineRef.getCameraLocked()
        this._onStateExit = () => {
            this.sprite.speed = oldSpeed
            this.sprite.entobs = oldObs
            this.invincible = oldInvincible
            this.engineRef.setCameraLocked(oldCameraLocked)
        }

        if (this.direction === Direction.UpLeft || this.direction === Direction.DownLeft) {
            this.direction = Direction.Left
        } else if (this.direction === Direction.UpRight || this.direction === Direction.DownRight) {
            this.direction = Direction.Right
        }

        this.stop()
        this.startAnimation('stand')

        if (this.stats.mp < 15 || !this.engineRef.hasSaveFlag('windrune')) {
            this.engine.sounds.menuBuzz.play()
            return
        }

        this.stats.mp -= 15

        this.engineRef.setCameraLocked(true)
        const delta = toDelta(this.direction)

        // charge

        this.engine.sounds.crushingGale.play()

        for (let i = 0; i < 30; ++i) {
            this.engine.map.xwin += delta.x * 2
            this.engine.map.ywin += delta.y * 2
            yield null
        }

        this.invincible = true
        this.sprite.entobs = false

        this.startAnimation('thrust')
        const r = galeRange[this.direction]
        this.move(this.direction, 100000)
        this.sprite.speed *= 10
        this.engineRef.setCameraLocked(false)
        for (let i = 0; i < 60; ++i) {
            const ents = this.detectCollision(r)
            for (let e of ents) {
                if (e.isKind('Enemy') && !e.invincible) {
                    e.hurt(this.stats.att + this.stats.mag * 2, 300, (this.direction + 2) & 3)
                }
            }

            yield null
            this.sprite.speed = Math.max(oldSpeed, this.sprite.speed - 20)
        }

        while (true) {
            const ents = this.detectCollision([0, 0, this.sprite.hotwidth, this.sprite.hotheight])
            let hasGap = false
            for (let e of ents) {
                if (e.isKind('Gap')) {
                    hasGap = true
                    break
                }
            }
            if (!hasGap) {
                break
            }
            yield null
        }

        this.stop()

        // stall
        for (let i = 0; i < 20; ++i) {
            yield null
        }
    }

    *healingRainState() {
        const oldInvincible = this.invincible
        this._onStateExit = () => {
            this.invincible = oldInvincible
        }

        this.stop()

        this.startAnimation('magic')

        if (this.stats.mp < 20 || !this.engineRef.hasSaveFlag('waterrune')) {
            this.engine.sounds.menuBuzz.play()
            return
        }

        this.stats.mp -= 20

        // not much to do here :)
        // TODO: particles or something, for confirmation for the player
        // if for no other reason.

        this.engine.sounds.healingRain.play()

        this.invincible = true

        for (let i = 0; i < 20; ++i) {
            yield null
        }

        let amount = this.stats.mag * 2 + 25
        amount += Math.floor(amount * random(-10, 10) * 0.01)
        this.stats.hp += Math.min(20, amount)

        const ents = this.detectCollision([-16, -16, 32, 32])

        for (let e of ents) {
            // TODO: Tidy
            if (e.isKind('IceChunks') && (e instanceof IceChunks)) {
                e.freeze()
                this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font, '~1The ice froze over!'))
                this.engineRef.destroyEntity(e)
                break
            }
        }

        for (let i = 0; i < 45; ++i) {
            yield null
        }
    }

    *shiverState() {
        this.stop()
        this.startAnimation('thrust')

        if (this.stats.mp < 45 || !this.engineRef.hasSaveFlag('cowardrune')) {
            this.engine.sounds.menuBuzz.play()
            return
        }

        this.stats.mp -= 45

        const ents = this.detectCollision([-160, -160, 320, 320])
        for (let e of ents) {
            if (e.isKind('Enemy') && !e.invincible) {
                const d = fromDelta(this.sprite.x - e.sprite.x, this.sprite.y - e.sprite.y)
                e.hurt((this.stats.att + this.stats.mag) * 3, 400, d)
            }
        }

        this.stop()

        // stall
        for (let i = 0; i < 100; ++i) {
            yield null
        }
    }

    die() {
        this.setState(this.deathState())
        this.engineRef.triggerGameLose()
    }

    *deathState() {
        this.invincible = true
        const s = this.hurtState(300, invert(this.direction))
        yield s.next()
        this.startAnimation('die')
        for (let _x of s) {
            yield null
        }

        while (true) {
            yield null
        }
    }

    *noOpState() {
        while (true) {
            yield null
        }
    }

    giveMPforHit() {
        this.stats.mp += random(0, 2 + Math.floor(this.stats.level/10))
    }
}
