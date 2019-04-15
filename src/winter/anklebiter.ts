import { makeAnimRange } from "./animator.js"
import { Direction, fromDelta, invert } from "./Direction.js"
import { Enemy } from "./enemy.js"
import { hypot, PyEngine, Sprite } from "./winter.js"

const _ankleBiterAnim: {[key: string]: [[number, number][][], boolean]} = {
    walk: [[
        makeAnimRange(10, 15, 10),
        makeAnimRange(15, 20, 10),
        makeAnimRange(5, 10, 10),
        makeAnimRange(0, 5, 10),
        makeAnimRange(10, 15, 10),
        makeAnimRange(15, 20, 10),
        makeAnimRange(10, 15, 10),
        makeAnimRange(15, 20, 10),
    ], true],

    idle: [[
        [[10, 1000]],
        [[15, 1000]],
        [[5, 1000]],
        [[0, 1000]],
        [[10, 1000]],
        [[15, 1000]],
        [[10, 1000]],
        [[15, 1000]],
    ], true],

    windup: [[
        [[30, 1000]],
        [[35, 1000]],
        [[25, 1000]],
        [[20, 1000]],
        [[30, 1000]],
        [[35, 1000]],
        [[30, 1000]],
        [[35, 1000]],
    ], true],

    attack: [[
        [[31, 20], [32, 15]],
        [[36, 20], [37, 15]],
        [[26, 20], [27, 15]],
        [[21, 20], [22, 15]],
        [[31, 20], [32, 15]],
        [[36, 20], [37, 15]],
        [[31, 20], [32, 15]],
        [[36, 20], [37, 15]],
        ],
        false
    ],

    hurt: [[
        [[38, 1000]],
        [[33, 1000]],
        [[23, 1000]],
        [[28, 1000]],
        [[38, 1000]],
        [[33, 1000]],
        [[38, 1000]],
        [[33, 1000]],
    ], false],

    die: [[
        [[38, 20], [39, 90]],
        [[33, 20], [34, 90]],
        [[23, 20], [24, 90]],
        [[28, 20], [29, 90]],
        [[38, 20], [39, 90]],
        [[33, 20], [34, 90]],
        [[38, 20], [39, 90]],
        [[33, 20], [34, 90]],
    ], false],
}

const _attackRange: [number, number, number, number][] = [
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
    [0, -8, 16, 8],
    [0, 16, 16, 8],
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
    [-8, 0, 8, 16],
    [16, 0, 8, 16],
]

export class AnkleBiter extends Enemy {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, _ankleBiterAnim)
        // Test code:
        // Equal probability of attacking or doing nothing.
        this.addMoods([this.attackMood.bind(this), this.passiveMood.bind(this)])

        this.setMood(this.passiveMood.bind(this))
        this.stats.maxhp = 20
        this.stats.hp = this.stats.maxhp
        this.stats.att = 7
        this.stats.exp = 1
    }

    isKind(kind: string) {
        return kind === 'AnkleBiter' || super.isKind(kind)
    }

    *hurtState(recoilSpeed: number, recoilDir: Direction) {
        if (this.stats.hp > 0) {
            this.engine.sounds['anklebiterHurt'].play()
        }
        if (this.stats.hp < Math.floor(this.stats.maxhp / 2)) {
            this.setMood(this.fleeMood.bind(this))
        }
        yield* super.hurtState(Math.floor(recoilSpeed * 1.5), recoilDir)
    }

    die() {
        // When one dies, the others scatter

        const ents = this.detectCollision([-50, -50, 100, 100])
        const allies = ents.filter(e => e.isKind('AnkleBiter') && e.stats.hp > 0)

        allies.forEach(a => {
            if (!(a instanceof AnkleBiter)) { throw new Error("Expected AnkleBiter"); }
            a.setMood(a.fleeMood.bind(a))
            a.setState(a.idleState())
        })

        super.die()
    }

    *attackMood() {
        // if we want to be uber, we can remove this hack.
        // for now fuckit.  Attack the player!!
        const p = this.engineRef.getPlayerEntity().js
        for (let q = 0; q < 5; ++q) {
            const d = fromDelta(p.sprite.x - this.sprite.x, p.sprite.y - this.sprite.y)
            const dist = hypot(p.sprite.x - this.sprite.x, p.sprite.y - this.sprite.y)
            if (dist < 40) {
                yield this.attackState(d)
                yield this.idleState(20)
            } else {
                yield this.walkState(d, Math.min(30, dist))
            }
        }
    }

    *fleeMood() {
        const MIN_DIST = 150
        const p = this.engineRef.getPlayerEntity().js
        for (let q = 0; q < 5; ++q) {
            const d = fromDelta(p.sprite.x - this.sprite.x, p.sprite.y - this.sprite.y)
            const dist = hypot(p.sprite.x - this.sprite.x, p.sprite.y - this.sprite.y)

            if (dist > MIN_DIST) {
                break
            }

            yield this.walkState(invert(d), MIN_DIST - dist)
        }

        this.setMood(this.passiveMood.bind(this))
        yield this.idleState()
    }

    *passiveMood() {
        const p = this.engineRef.getPlayerEntity().js
        this.stopAnimation()
        while (true) {
            const dist = hypot(p.sprite.x - this.sprite.x, p.sprite.y - this.sprite.y)

            yield this.idleState()

            if (dist < 150) {
                this.engine.sounds['anklebiterStrike'].play()
                this.setMood(this.attackMood.bind(this))
                yield this.idleState()
                break
            }
        }
    }

    *idleState(time: number = 50) {
        this.stopAnimation()
        yield* super.idleState(time)
    }

    *walkState(dir: Direction, dist: number) {
        const [ox, oy] = [this.sprite.x, this.sprite.y]
        this.move(dir, dist)
        this.startAnimation('walk')
        while (this.isMoving()) {
            yield null
            if (ox === this.sprite.x && oy === this.sprite.y) {
                break
            }
        }
        this.stop()
    }

    *deathState() {
        this.engine.sounds['anklebiterDie'].play()
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

        this.engine.sounds['anklebiterStrike'].play()

        this.sprite.speed *= 2

        // Winding up for the pounce.
        for (let i = 0; i < 30; ++i) {
            yield null
        }

        this.startAnimation('attack')
        this.move(dir, 32)
        while (this.isAnimating()) {
            const ents = this.detectCollision(_attackRange[dir])

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
