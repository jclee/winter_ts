import { Animator } from "./animator.js"
import { Direction, invert, toDelta } from "./Direction.js"
import { StatSet } from "./statset.js"
import { Engine, PyEngine, Sprite } from "./winter.js"

// arbitrary, and meaningless for the most part.
const _DIST = 48

export class Entity {
    // Most every interactive thing in the game is an Entity.

    protected engine: Engine
    public stats: StatSet
    private _animator: Animator
    private _anim: {[key: string]: [[number, number][][], boolean]}
    public direction: Direction
    public interruptable: boolean
    public invincible: boolean
    protected _state: IterableIterator<any> | null
    protected _onStateExit: (()=>void) | null

    constructor(
        protected engineRef: PyEngine,
        public sprite: Sprite,
        anim: {[key: string]: [[number, number][][], boolean]},
    ) {
        this.engine = engineRef.getEngine().js

        this.stats = new StatSet()
        this.stats.hp = 1

        this._animator = new Animator()
        this._anim = anim
        this.direction = Direction.Down // as good as any
        this.interruptable = true // if false, no state changes will occur
        this.invincible = false
        this._state = null
        this._onStateExit = null
        this.setState(this.defaultState())
    }

    isKind(_kind: string) {
        return false // Well... technically "Entity", but no one cares.
    }

    update() {
        // Main update routine.  Override if you must, use the state mechanism if you can.
        this.animate()
        if (this._state === null) {
            this.setState(this.defaultState())
            if (this._state === null) { throw new Error("unexpected null state") }
        }
        if (this._state.next().done) {
            this.setState(this.defaultState())
            if (this._state === null) { throw new Error("unexpected null state") }
            this._state.next()
        }
    }

    die() {
        this.engineRef.pyDestroyEntity(this)
    }

    // if recoil is nonzero, the enemy is blown backwards in a direction,
    // at some speed.  The default direction is backwards
    hurt(amount: number, recoilSpeed: number = 0, recoilDir: Direction | null = null) {
        if (this.invincible) { return }

        if (recoilDir === null) {
            recoilDir = invert(this.direction)
        }

        if (this.stats.hp <= amount) {
            this.stats.hp = 0
            this.die()
        } else {
            this.stats.hp -= amount
            this.setState(this.hurtState(recoilSpeed, recoilDir))
        }
    }

    setState(newState: IterableIterator<any>) {
        if (this._onStateExit !== null) {
            this._onStateExit()
            this._onStateExit = null
        }
        if (this.interruptable || this._state === null) {
            this._state = newState
        }
    }

    *defaultState() {
        while (true) { yield null }
    }

    *hurtState(recoilSpeed: number, recoilDir: Direction) {
        const oldSpeed = this.sprite.speed
        const oldInvincible = this.invincible
        this._onStateExit = () => {
            this.sprite.speed = oldSpeed
            this.invincible = oldInvincible
        }

        this.sprite.speed = recoilSpeed
        this.move(recoilDir, 1000000) // just go until I say stop
        this.startAnimation('hurt')

        this.invincible = true
        let t = 64
        while (true) {
            t -= 1
            if (t <= 34) { this.invincible = oldInvincible }
            this.sprite.speed -= Math.floor(t / 8)

            yield null

            if (t <= 0 || this.sprite.speed <= 0) { break }
        }

        this.direction = invert(this.direction)
        this.sprite.Stop()
        yield null
    }

    detectCollision(rect: [number, number, number, number]) {
        // Returns a list of entities that are within the rect.
        // The rect's position is taken as being relative to the
        // entity's position.  This is useful for attacks and such.

        const x = rect[0] + this.sprite.x
        const y = rect[1] + this.sprite.y
        const w = rect[2]
        const h = rect[3]
        const layer = this.sprite.layer

        const entities: Entity[] = []
        this.engine.map.spritesAt(x, y, w, h, layer).forEach(s => {
            const ent = this.engineRef.getEntityForSpriteName(s.name).js
            if (ent) {
                entities.push(ent)
            }
        })
        return entities
    }

    touches(ent: Entity) {
        return this.sprite.touches(ent.sprite)
    }

    // Entity methods.  Most everything that involves an ika sprite should be done here.
    up() { this.move(Direction.Up) }
    down() { this.move(Direction.Down) }
    left() { this.move(Direction.Left) }
    right() { this.move(Direction.Right) }
    upLeft() { this.move(Direction.UpLeft) }
    upRight() { this.move(Direction.UpRight) }
    downLeft() { this.move(Direction.DownLeft) }
    downRight() { this.move(Direction.DownRight) }

    move(d: Direction, dist: number = _DIST) {
        const delta = toDelta(d)
        this.direction = d
        this.sprite.moveTo(
            Math.floor(this.sprite.x + dist * delta.x),
            Math.floor(this.sprite.y + dist * delta.y)
        )
    }

    isMoving() {
        return this.sprite.isMoving
    }
    stop() {
        this.sprite.Stop()
    }

    animate() {
        this._animator.update()
        this.sprite.specframe = this._animator.curFrame
    }

    startAnimation(name: string) {
        const [a, loop] = this._anim[name]
        this._animator.start(a[this.direction], loop)
    }

    stopAnimation() {
        this._animator.stop()
    }

    isAnimating() {
        return this._animator.isAnimating
    }

    getAnimationIndex() {
        return this._animator.index
    }
}
