import { Caption } from "./caption.js"
import { Entity } from "./entity.js"
import { PyEngine, Sprite } from "./winter.js"

class Obstacle extends Entity {
    public flagName: string

    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
        anim: {[key: string]: [[number, number][][], boolean]} = {},
    ) {
        super(engineRef, sprite, anim)
        this.flagName = this.sprite.name
        this.invincible = true

        if (engineRef.getSaveFlag(this.flagName) !== '') {
            this.remove()
        }
    }

    remove() {
        this.sprite.x = -100
        this.sprite.y = -100
        this.engineRef.pyDestroyEntity(this)
    }

    update() {}
}

export class IceWall extends Obstacle {
    // Not very exciting.  The entity's type is all the information
    // we need.

    isKind(kind: string) {
        return kind == 'IceWall' || super.isKind(kind)
    }
}

export class Gap extends Obstacle {
    // A big empty hole. :P

    isKind(kind: string) {
        return kind == 'Gap' || super.isKind(kind)
    }
}

const _iceChunksAnim: {[key: string]: [[number, number][][], boolean]} = {
    default: [[
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
        [[0, 50], [1, 50]],
    ], true],
}

const _frozenTiles = [
    [145, 149, 144],
    [142, 113, 143],
    [139, 148, 138],
]

export class IceChunks extends Obstacle {
    constructor(
        engineRef: PyEngine,
        sprite: Sprite,
    ) {
        super(engineRef, sprite, _iceChunksAnim)
        this.startAnimation('default')
    }

    isKind(kind: string) {
        return kind == 'IceChunks' || super.isKind(kind)
    }

    remove() {
        this.freeze()
        super.remove()
    }

    freeze() {
        const lay = this.sprite.layer
        const tx = Math.floor(this.sprite.x / 16)
        const ty = Math.floor(this.sprite.y / 16)
        for (let y = 0; y < 3; ++y) {
            for (let x = 0; x < 3; ++x) {
                this.engine.map.SetTile(x + tx, y + ty, lay, _frozenTiles[y][x])
                this.engine.map.SetObs(x + tx, y + ty, lay, 0)
            }
        }

        this.engineRef.setSaveFlag(this.flagName, 'True')
    }
}

export class Boulder extends Obstacle {
    update() {
        if (this.touches(this.engineRef.getPlayerEntity().js)) {
            // find a stick of TNT
            for (let key of ['dynamite0', 'dynamite1', 'dynamite2', 'dynamite3']) {
                if (this.engineRef.getSaveFlag(key) !== 'True') {
                    continue;
                }

                // TODO: explode animation here
                this.engineRef.setSaveFlag(key, 'False')
                this.engineRef.setSaveFlag(this.flagName, 'Broken')
                this.engineRef.pyDestroyEntity(this)
                this.engineRef.addThing(new Caption(this.engineRef, this.engineRef.font.js, 'Blew the rock apart!'))
            }
        }
    }
}
