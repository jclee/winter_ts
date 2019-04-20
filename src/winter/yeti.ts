import { makeAnimRange } from "./animator.js"
import { Direction, fromDelta } from "./Direction.js"
import { Enemy } from "./enemy.js"
import { hypot, PyEngine, Sprite } from "./winter.js"

const _anim: {[key: string]: [[number, number][][], boolean]} = {
    idle: [[
        [[7, 1000]],
        [[14, 1000]],
        [[21, 1000]],
        [[0, 1000]],
        [[7, 1000]],
        [[14, 1000]],
        [[7, 1000]],
        [[14, 1000]],
    ], true],

    walk: [[
        makeAnimRange(8, 14, 15),
        makeAnimRange(15, 21, 15),
        makeAnimRange(22, 28, 15),
        makeAnimRange(1, 7, 15),
        makeAnimRange(8, 14, 15),
        makeAnimRange(15, 21, 15),
        makeAnimRange(8, 14, 15),
        makeAnimRange(15, 21, 15),
    ], true],

    hurt: [[
        [[45, 1000]],
        [[38, 1000]],
        [[31, 1000]],
        [[52, 1000]],
        [[45, 1000]],
        [[38, 1000]],
        [[45, 1000]],
        [[38, 1000]],
    ], true],

    die: [[
        [[38, 30], [39, 90]],
        [[45, 30], [46, 90]],
        [[52, 30], [53, 90]],
        [[31, 30], [32, 90]],
        [[38, 30], [39, 90]],
        [[45, 30], [46, 90]],
        [[38, 30], [39, 90]],
        [[45, 30], [46, 90]],
    ], false],

    windup: [[
        [[35, 25],[36, 10]],
        [[42, 25],[43, 10]],
        [[49, 25],[50, 10]],
        [[28, 25],[29, 10]],
        [[35, 25],[36, 10]],
        [[42, 25],[43, 10]],
        [[35, 25],[36, 10]],
        [[42, 25],[43, 10]],
    ], false],

    attack: [[
        [[37, 20],],
        [[44, 20],],
        [[51, 20],],
        [[30, 20],],
        [[37, 20],],
        [[44, 20],],
        [[37, 20],],
        [[44, 20],],
    ], false],
}

const _attackRange: [number, number, number, number][] = [
    [-24, 0, 24, 32],
    [32, 0, 24, 32],
    [-22, -24, 52, 24],
    [-22, 32, 52, 24],
    [-24, 0, 24, 32],
    [32, 0, 24, 32],
    [-24, 0, 24, 32],
    [32, 0, 24, 32],
]

export class Yeti extends Enemy {
    protected dieSound: string
    protected hurtSound: string
    protected strikeSound: string

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, _anim)
        this.sprite.speed = 80

        this.addMoods([this.attackMood.bind(this), this.passiveMood.bind(this)])

        this.stats.maxhp = 100
        this.stats.hp = this.stats.maxhp
        this.stats.att = 20
        this.stats.exp = 100
        this.dieSound = 'yetiDie'
        this.hurtSound = 'yetiHurt'
        this.strikeSound = 'yetiStrike'
    }

    *hurtState(dist: number, dir: Direction) {
        if (this.stats.hp > 0) {
            this.engine.sounds[this.hurtSound].play()
        }

        this.setMood(this.attackMood.bind(this))
        yield* super.hurtState(Math.floor(dist * 2 / 3), dir)
    }

    *attackMood() {
        // if we want to be uber, we can remove this hack.
        // for now fuckit.  Attack the player!!
        const p = this.engineRef.getPlayerEntity()
        for (let q = 0; q < 5; ++q) {
            // compensate for the yeti's gigantic sprite:
            const sx = this.sprite.x + 16
            const sy = this.sprite.y + 16
            const d = fromDelta(p.sprite.x - sx, p.sprite.y - sy)
            const dist = hypot(p.sprite.x - sx, p.sprite.y - sy)
            if (dist < 50) {
                yield this.attackState(d)
                yield this.idleState(20)
            } else {
                yield this.walkState(d, Math.min(90, dist))
            }
        }
    }

    *passiveMood() {
        const p = this.engineRef.getPlayerEntity()
        this.stopAnimation()
        while (true) {
            // compensate for the yeti's gigantic sprite:
            const sx = this.sprite.x + 16
            const sy = this.sprite.y + 16
            const dist = hypot(p.sprite.x - sx, p.sprite.y - sy)

            yield this.idleState()

            if (dist < 150) {
                this.setMood(this.attackMood.bind(this))
                yield this.idleState()
                return
            }
        }
    }

    *deathState() {
        this.engine.sounds[this.dieSound].play()
        this.startAnimation('die')
        yield* super.deathState()
    }

    *walkState(dir: Direction, dist: number) {
        this.move(dir, dist)
        this.startAnimation('walk')
        dist *= 100
        while (dist > 0) {
            dist -= this.sprite.speed
            yield null
        }
        this.stop()
    }

    *attackState(dir: Direction) {
        const oldInterruptable = this.interruptable
        this._onStateExit = () => {
            this.interruptable = oldInterruptable
        }

        this.direction = dir
        this.startAnimation('windup')
        this.stop()
        this.engine.sounds[this.strikeSound].play()
        this.interruptable = false

        // Wind up.  Hold up a sec.
        for (let i = 0; i < 35; ++i) {
            yield null
        }

        this.startAnimation('attack')
        this.move(dir, 6)
        for (let i = 0; i < 20; ++i) {
            for (let e of this.detectCollision(_attackRange[dir])) {
                if (e.isKind('Player')) {
                    const d = Math.max(1, this.stats.att - e.stats.pres)
                    e.hurt(d, 350, this.direction)
                }
            }
            yield null
        }

        this.stop()

        this.setState(this.idleState(10))
        yield null
    }
}

export class Gorilla extends Yeti {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite)
        this.sprite.speed = 90
        this.stats.maxhp = 300
        this.stats.hp = 200
        this.stats.att = 36
        this.stats.exp = 200
    }
}

export class SoulReaver extends Yeti {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite)
        this.sprite.speed = 120
        this.stats.maxhp = 1500
        this.stats.hp = 1500
        this.stats.att = 60
        this.stats.exp = 750
        this.dieSound = 'soulReaverDie'
        this.hurtSound = 'soulReaverHurt'
        this.strikeSound = 'soulReaverStrike'
    }
        
    *attackState(direc: Direction) {
        this.direction = direc
        if (this.direction === Direction.UpLeft || this.direction == Direction.DownLeft) {
            this.direction = Direction.Left
        } else if (this.direction == Direction.UpRight || this.direction == Direction.DownRight) {
            this.direction = Direction.Right
        }

        const oldInterruptable = this.interruptable
        this._onStateExit = () => {
            this.interruptable = oldInterruptable
        }

        this.startAnimation('windup')
        this.stop()
        this.engine.sounds[this.strikeSound].play()
        this.interruptable = false

        // Wind up.  Hold up a sec.
        // Show first frame for a bit longer than usual.
        this.stopAnimation()
        for (let i = 0; i < 75; ++i) {
            yield null
        }
        this.startAnimation('windup')
        for (let i = 0; i < 35; ++i) {
            yield null
        }

        this.startAnimation('attack')
        this.sprite.speed += 800
        this.move(this.direction, 2000)

        for (let i = 0; i < 8; ++i) {
            this.sprite.speed -= (i + 2) * 10
            for (let e of this.detectCollision(_attackRange[this.direction])) {
                if (e.isKind('Player')) {
                    const d = Math.max(1, this.stats.att - e.stats.pres)
                    e.hurt(d, 350, this.direction)
                }
            }
            yield null
        }

        for (let i = 0; i < 30; ++i) {
            this.sprite.speed = Math.max(10, this.sprite.speed - 10)
            yield null
        }

        this.stop()

        this.setState(this.idleState(10))
        this.sprite.speed = 120

        yield null
    }
}
