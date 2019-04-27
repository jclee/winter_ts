import { Caption } from "./caption.js"
import { Entity } from "./entity.js"
import { PyEngine, Sprite } from "./winter.js"

class Rune extends Entity {
    protected name: string

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, {})
        this.invincible = true
        this.name = this.sprite.name

        if (engineRef.getSaveFlag(this.name)) {
            this.sprite.x = -100
            this.engineRef.destroyEntity(this)
        }
    }

    getElement() { return '' }
    apply() {}

    update() {
        if (this.touches(this.engineRef.getPlayerEntity())) {
            this.engineRef.destroyEntity(this)
            this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font, `~1You got the ${this.getElement()} Rune!`))
            this.engineRef.setSaveFlag(this.name, 'True')
            this.apply()
        }
    }
}

export class WaterRune extends Rune {
    getElement() { return 'Water' }
}

export class FireRune extends Rune {
    getElement() { return 'Fire' }
}

export class WindRune extends Rune {
    getElement() { return 'Wind' }
}

export class CowardRune extends Rune {
    getElement() { return 'Coward' }
}

export class BindingRune extends Rune {
    getElement() { return 'Binding' }
}

export class StrengthRune extends Rune {
    apply() {
        this.engineRef.getPlayerEntity().stats.att += 2
    }
    getElement() { return 'Strength' }
}

export class GuardRune extends Rune {
    apply() {
        this.engineRef.getPlayerEntity().stats.pres += 2
        this.engineRef.getPlayerEntity().stats.mres += 2
    }
    getElement() { return 'Guard' }
}

export class PowerRune extends Rune {
    apply() {
        this.engineRef.getPlayerEntity().stats.mag += 2
    }
    getElement() { return 'Power' }
}
