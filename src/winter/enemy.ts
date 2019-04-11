import { Direction } from "./Direction.js"
import { Entity } from "./entity.js"
import { PyEngine, Sprite, random} from "./winter.js"

export class Enemy extends Entity {
    // Enemy baseclass.  Enemies are entities that die.

    // Enemies also have a brain.  Unlike the player, the state generators
    // are allowed to end, at which point the brain is queried as to what to do
    // next.

    // Maybe it would be a good idea to send the brain information about why
    // it is reconsidering its options.

    private _mood: IterableIterator<any> | null
    private _moods: (()=>IterableIterator<any>)[]

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
        anim: {[key: string]: [[number, number][][], boolean]},
    ) {
        super(engineRef, sprite, anim)
        this.setState(this.idleState())
        this.stats.hp = 15
        this._mood = null
        this._moods = []
    }

    isKind(kind: string) {
        return kind === 'Enemy' || super.isKind(kind)
    }

    setMood(gen: (()=>IterableIterator<any>) | null) {
        if (gen === null) {
            this._mood = null
        } else {
            this._mood = gen()
        }
    }

    addMoods(moods: (()=>IterableIterator<any>)[]) {
        this._moods = this._moods.concat(moods)
    }

    think() {
        if (this._mood !== null) {
            const result = this._mood.next()
            if (!result.done) {
                this.setState(result.value)
                return
            }
        }
        //this.interruptable = true
        const n = random(0, this._moods.length)
        this.setMood(this._moods[n])
        if (this._mood === null) {
            throw new Error("Unexpected null mood")
        }
        const result = this._mood.next()
        if (result.done) {
            throw new Error("Unexpected end of iterator")
        }
        this.setState(result.value)
    }

    die() {
        this._mood = null
        this.interruptable = true
        this.setState(this.deathState())
        this.engineRef.pyGivePlayerXP(this.stats.exp)
        //this.engineRef.player.stats.mp += this.stats.exp // MP Regen for the player.
    }

    *deathState() {
        this.invincible = true
        this.interruptable = false

        // do the hurt animation
        const dummy = this.hurtState(0, this.direction)

        // let it go for a moment
        const result = dummy.next()
        if (result.done) {
            throw new Error("Unexpected end of iterator")
        }
        yield result.value

        this.stats.hp = 0

        // take over the animation, then finish the hurt state
        this.startAnimation('die')
        yield* dummy

        this.sprite.isobs = false
        // burn cycles until the engine kills us
        while (true) {
            yield null
        }
    }

    update() {
        this.animate()
        if (this._state === null) {
            this.think()
        }
        if (this._state === null) {
            throw new Error("Unexpected null state")
        }
        const result = this._state.next()
        if (result.done) {
            this.think()
        }
    }

    *defaultState() {
        yield null
    }

    *idleState(time = 50) {
        this.startAnimation('idle')
        while (time > 0) {
            time -= 1
            yield null
        }
    }

    hurt(amount: number, speed: number = 0, dir: Direction | null = null) {
        this.engine.sounds['monsterHit'].play()
        super.hurt(amount, speed, dir)
    }
}
