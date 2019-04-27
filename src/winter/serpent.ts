import { makeAnim, makeAnimRange } from "./animator.js"
import { AnkleBiter, Carnivore } from "./anklebiter.js"
import { Direction, fromDelta } from "./Direction.js"
import { Enemy } from "./enemy.js"
import { PyEngine, random, Sprite } from "./winter.js"

// arbitrary :D
const _idleAnim = makeAnim([0, 4, 0, 0, 0, 4, 0, 0, 1, 2, 3, 2, 1, 0], 50)
const _biteAnim = makeAnimRange(16, 22, 7) // could do some speed-tinkering here.  Make the first and last frames slower than the middle ones.
const _stareAnim = makeAnim([4, 5, 5, 6, 6, 7, 5, 4], 20)
const _roarAnim = makeAnim([12, 13, 13, 14, 15, 16, 16, 16, 14, 12], 20)
const _deathAnim = makeAnimRange(24, 27, 100)
const _appearAnim = makeAnim([26, 25, 24], 20)
const _hurtAnim = makeAnim([10], 50)

const _anim: {[key: string]: [[number, number][][], boolean]} = {
    idle: [Array(8).fill(_idleAnim), true],
    bite: [Array(8).fill(_biteAnim), false],
    stare: [Array(8).fill(_stareAnim), false],
    roar: [Array(8).fill(_roarAnim), false],
    die: [Array(8).fill(_deathAnim), false],
    appear: [Array(8).fill(_appearAnim), false],
    hurt: [Array(8).fill(_hurtAnim), false],
}

const _biteRange: [number, number, number, number][] = [
    [0, 41, 30, 0],
    [0, 41, 30, 6],
    [0, 41, 30, 20],
    [0, 41, 30, 30],
    [0, 41, 30, 0],
    [0, 41, 30, 0],
]

export class Serpent extends Enemy {
    private bleh: IterableIterator<any>

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, _anim)

        this.addMoods([this.watchMood.bind(this)])

        this.stats.maxhp = 300
        this.stats.hp = this.stats.maxhp
        this.stats.att = 35
        this.invincible = true

        sprite.mapobs = false
        sprite.entobs = false
        this.bleh = this.watchMood()
    }

    die() {
        this.engineRef.triggerGameWin()
    }

    think() {
        const { value } = this.bleh.next()
        this.setState(value)
    }

    *hurtState(_recoilSpeed: number, _recoilDir: Direction) {
        this.startAnimation('hurt')
        this.invincible = true
        this.interruptable = false
        let i = 30
        while (i > 0) {
            i -= 1
            yield null
        }

        this.interruptable = true
    }

    *watchMood() {
        // Go left to right, try to vertically align with the player,
        // then try to bite.
        // Roar every now and again.
        const p = this.engineRef.getPlayerEntity()

        while (true) {
            // why is this necessary? O_o
            //this.interruptable = true
            //this._state = null

            const count = random(1, 8)
            for (let n = 0; n < count; ++n) {
                const x = this.sprite.x + Math.floor(this.sprite.hotwidth / 2)
                const d = fromDelta(p.sprite.x - x, 0)
                yield this.moveState(d, Math.abs(p.sprite.x - x))

                if (random(0, 100) < 70) {
                    yield this.biteState()
                }
            }

            yield this.roarState()
        }
    }

    *moveState(dir: Direction, dist: number) {
        this.startAnimation('idle')
        this.move(dir, dist)

        dist *= 100
        while (dist > 0) {
            dist -= this.sprite.speed
            yield null
        }
    }

    *biteState() {
        this.startAnimation('bite')
        this.invincible = false

        while (this.isAnimating()) {
            for (let e of this.detectCollision(_biteRange[this.getAnimationIndex()])) {
                const d = Math.max(1, this.stats.att - this.engineRef.getPlayerEntity().stats.pres)
                e.hurt(d, 350, Direction.Down)
            }
            yield null
        }

        for (let i = 0; i < 60; ++i) {
            yield null
        }

        this.invincible = true
    }

    *stareState() {
        this.startAnimation('stare')
        // TODO: finish this if someone can think of a good idea for
        // what it should do!
        yield null
    }

    *roarState() {
        // spawn one to five Carnivores to irritate the shit out of the player
        this.startAnimation('roar')

        const offsets = [0, 1, 1, 2, 3, 4, 4, 4, 2, 0]
        for (let wait = 0; wait < 200; ++wait) {
            const offset = offsets[Math.floor(wait / 20)]
            this.engine.map.xwin += random(-offset, offset + 1)
            this.engine.map.ywin += random(-offset, offset + 1)
            yield null
        }

        const count = random(1, 4)
        for (let q = 0; q < count; ++q) {
            const [x, y] = [320 + (q * 60), 588]
            const sprites = this.engine.map.spritesAt(x, y, x + 16, y + 16, this.sprite.layer)

            if (sprites.length === 0) {
                let e: AnkleBiter
                if (random(0, 2)) {
                    e = new Carnivore(this.engineRef, this.engine.map.addSprite(x, y, this.sprite.layer, 'carnivore.ika-sprite'))
                } else {
                    e = new AnkleBiter(this.engineRef, this.engine.map.addSprite(x, y, this.sprite.layer, 'anklebiter.ika-sprite'))
                }
                this.engineRef.addEntity(e)
                e.setMood(e.attackMood.bind(e))
            }
        }

        // need to destroy old corpses (a first!)
        for (let e of this.engineRef.getEntities()) {
            if (e.stats.hp === 0 && e.isKind('Enemy')) {
                this.engineRef.destroyEntity(e)
            }
        }
    }
}
