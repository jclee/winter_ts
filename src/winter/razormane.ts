import { makeAnimRange } from "./animator.js"
import { Direction, fromDelta, invert } from "./Direction.js"
import { Enemy } from "./enemy.js"
import { hypot, PyEngine, random, Sprite } from "./winter.js"

const razorManeAnim: {[key: string]: [[number, number][][], boolean]} = {
    walk: [[
        makeAnimRange(7, 14, 9),
        makeAnimRange(14, 21, 9),
        makeAnimRange(21, 28, 9),
        makeAnimRange(0, 7, 9),
        makeAnimRange(7, 14, 9),
        makeAnimRange(14, 21, 9),
        makeAnimRange(7, 14, 9),
        makeAnimRange(14, 21, 9),
    ], true],

    idle: [[
        [[7, 1000]],
        [[14, 1000]],
        [[21, 1000]],
        [[0, 1000]],
        [[7, 1000]],
        [[14, 1000]],
        [[7, 1000]],
        [[14, 1000]],
    ], false],

    windup: [[
        [[35, 30]],
        [[42, 30]],
        [[28, 30]],
        [[49, 30]],
        [[35, 30]],
        [[42, 30]],
        [[35, 30]],
        [[42, 30]],
    ], false],

    attack: [[
        [[36, 20]],
        [[43, 20]],
        [[29, 20]],
        [[50, 20]],
        [[36, 20]],
        [[43, 20]],
        [[36, 20]],
        [[43, 20]],
    ], false],

    hurt: [[
        [[44, 1000]],
        [[37, 1000]],
        [[51, 1000]],
        [[30, 1000]],
        [[44, 1000]],
        [[37, 1000]],
        [[44, 1000]],
        [[37, 1000]],
    ], false],

    die: [[
        [[44, 20], [45, 90]],
        [[37, 20], [38, 90]],
        [[51, 20], [52, 90]],
        [[30, 20], [31, 90]],
        [[44, 20], [45, 90]],
        [[37, 20], [38, 90]],
        [[44, 20], [45, 90]],
        [[37, 20], [38, 90]],
    ], false],
}

const attackRange: [number, number, number, number][] = [
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
    [0, -8, 16, 8],
    [0, 16, 16, 8],
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
]

export class RazorMane extends Enemy {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, razorManeAnim)

        this.addMoods([this.stalkMood.bind(this), this.passiveMood.bind(this)])

        this.setMood(this.passiveMood.bind(this))
        this.sprite.speed = 150
        this.stats.maxhp = this.stats.hp = 60
        this.stats.att = 20
        this.stats.exp = 13
    }

    isKind(kind: string) {
        return kind == 'RazorMane' || super.isKind(kind)
    }

    *hurtState(recoilSpeed: number, recoilDir: Direction) {
        if (this.stats.hp > 0) {
            this.engine.sounds['razorManeHurt'].play()
        }
        if (this.stats.hp < Math.floor(this.stats.maxhp / 2)) {
            this.setMood(this.fleeMood.bind(this))
        }
        yield* super.hurtState(recoilSpeed, recoilDir)
    }

    die() {
        // When one dies, the others scatter

        const ents = this.detectCollision([-50, -50, 100, 100])
        const allies = ents.filter(e => e.isKind('RazorMane') && e.stats.hp > 0)

        for (let a of allies) {
            if (!(a instanceof RazorMane)) { throw new Error("Expected RazorMane"); }
            a.setMood(a.fleeMood.bind(a))
            a.setState(a.idleState())
        }

        super.die()
    }

    playerDir() {
        const p = this.engineRef.getPlayerEntity()
        return fromDelta(p.sprite.x - this.sprite.x - 10, p.sprite.y - this.sprite.y - 7)
    }

    playerDist() {
        const p = this.engineRef.getPlayerEntity()
        return hypot(p.sprite.x - this.sprite.x - 10, p.sprite.y - this.sprite.y - 7)
    }

    *attackMood() {
        for (let q = 0; q < 5; ++q) {
            const d = this.playerDir()
            const dist = this.playerDist()
            if (dist < 40) {
                yield this.attackState(d)
                yield this.idleState(20)
            } else {
                yield this.walkState(d, Math.min(30, dist))
            }
        }
    }

    *stalkMood() {
        const DIST = 0
        // be DIST away, if at all possible
        while (true) {
            const d = this.playerDir()
            const dist = this.playerDist()

            if (dist - DIST > 60) {
                // get closer
                const n = dist - DIST - 1
                yield this.walkState(d, random(Math.floor(n / 2), n))

                yield this.idleState(60)
            } else if (dist < DIST) {
                // fall back

                yield this.walkState(invert(d), Math.min(80, DIST - dist))
                this.direction = d
                yield this.idleState(60)
            } else {
                this.setMood(this.attackMood.bind(this))
                yield this.idleState(1)
            }
        }
    }

    *fleeMood() {
        const MIN_DIST = 150
        for (let q = 0; q < 5; ++q) {
            const d = this.playerDir()
            const dist = this.playerDist()

            if (dist > MIN_DIST) {
                break
            }

            yield this.walkState(invert(d), MIN_DIST - dist)
        }

        this.setMood(this.passiveMood.bind(this))
        yield this.idleState()
    }

    *passiveMood() {
        this.stopAnimation()
        while (true) {
            const dist = this.playerDist()

            yield this.idleState()

            if (dist < 150) {
                this.setMood(this.stalkMood.bind(this))
                yield this.idleState()
                return
            }
        }
    }

    *idleState(time = 50) {
        this.stopAnimation()
        yield* super.idleState(time)
    }

    *walkState(dir: Direction, dist: number) {
        const ox = this.sprite.x
        const oy = this.sprite.y
        this.move(dir, dist)
        this.startAnimation('walk')
        dist *= 100
        while (dist > 0) {
            dist -= this.sprite.speed
            yield null
            if (ox === this.sprite.x && oy === this.sprite.y) {
                break
            }
        }

        this.stop()
    }

    *deathState() {
        this.engine.sounds['razorManeDie'].play()
        this.startAnimation('die')
        yield* super.deathState()
    }

    *attackState(dir: Direction) {
        const oldSpeed = this.sprite.speed
        this._onStateExit = () => {
            this.sprite.speed = oldSpeed
        }

        this.direction = dir
        this.startAnimation('windup')
        this.stop()

        this.engine.sounds['razorManeStrike'].play()

        this.sprite.speed *= 2

        // Winding up for the pounce.
        for (let i = 0; i < 30; ++i) {
            yield null
        }

        this.startAnimation('attack')
        this.move(dir, 32)
        while (this.isAnimating()) {
            const ents = this.detectCollision(attackRange[dir])

            for (let e of ents) {
                if (e.isKind('Player')) {
                    const d = Math.max(1, this.stats.att - e.stats.pres)
                    e.hurt(d, 150, this.direction)
                    yield null
                    return
                }
            }

            yield null
        }
        this.stop()
    }
}

export class HellHound extends RazorMane {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite)
        this.sprite.speed = 180
        this.stats.maxhp = 300
        this.stats.hp = 300
        this.stats.att = 33
        this.stats.exp = 80
    }
}

export class DragonPup extends RazorMane {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite)
        this.sprite.speed = 160
        this.stats.maxhp = 160
        this.stats.hp = 160
        this.stats.att = 28
        this.stats.exp = 34
    }
}
