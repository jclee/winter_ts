import { Caption } from "./caption.js"
import { Entity } from "./entity.js"
import { PyEngine, Sprite } from "./winter.js"

export class Dynamite extends Entity {
    private flagName: string

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, {})
        this.flagName = sprite.name
        this.invincible = true

        if (this.engineRef.getSaveFlag(this.flagName)) {
            sprite.x = sprite.y = -100
            this.engineRef.pyDestroyEntity(this)
        }
    }

    update() {
        if (this.touches(this.engineRef.getPlayerEntity().js)) {
            this.engineRef.setSaveFlag(this.flagName, 'True')
            this.engineRef.pyDestroyEntity(this)
            this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font.js, '~1Got a stick of dynamite!'))
        }
    }
}