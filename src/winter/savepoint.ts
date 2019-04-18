import { invert, toDelta } from "./Direction.js"
import { Entity } from "./entity.js"
import { PyEngine, Sprite } from "./winter.js"

export class SavePoint extends Entity {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, {})
        this.interruptable = false
        this.invincible = true
    }

    update() {
        const p = this.engineRef.getPlayerEntity().js
        if (this.touches(p)) {
            p.stats.hp = 999
            p.stats.mp = 999

            // bump the player backward, so he's not touching us anymore.
            const delta = toDelta(invert(p.direction))
            p.sprite.x = p.sprite.x + delta.x * 3
            p.sprite.y = p.sprite.y + delta.y * 3

            this.engineRef.setShowSaveMenuAtEndOfTick(true)
        }
    }
}
