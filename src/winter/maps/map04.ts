import { MapScript } from "./mapscript.js"
import { Thing } from "./../thing.js"
import { PyEngine, Snow } from "./../winter.js"
import { SoulReaver, Yeti } from "./../yeti.js"

export default new MapScript(autoexec, { to3, to5 })

export function autoexec(engineRef: PyEngine) {
    engineRef.addMapThing(new Snow(engineRef, 8000, [-.2, 3]))
    if (!engineRef.hasSaveFlag('waterrune')) {
        engineRef.addMapThing(new RuneListener(engineRef))
    }
    if (engineRef.hasSaveFlag('nearend')) {
        engineRef.addMapThing(new RuneListener(engineRef))
    }
}

export function *to3(engineRef: PyEngine) {
    const offset_from = 11 * 16  // first horizontal pos possible
    const offset_to = 8 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map03.ika-map', [x, 1 * 16])
}

export function *to5(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map05.ika-map', [10 * 16, 19 * 16])
}

class DeathListener extends Thing {
    // Waits until the yeti is dead, then drops the fire rune.
    constructor(private engineRef: PyEngine, private yeti: Yeti) { super() }

    update() {
        if (this.yeti.stats.hp === 0) {
            this.engineRef.pyPlayMusic("music/winter.ogg")
            this.engineRef.setSaveFlag('waterguard', 'True')
            return true
        }
        return false
    }
}

class RuneListener extends Thing {
    constructor(private engineRef: PyEngine) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        if (this.engineRef.hasSaveFlag('nearend')
            && !this.engineRef.hasSaveFlag('waterguard')
        ) {
            this.engineRef.pyPlayMusic("music/resurrection.it")
            const p = this.engineRef.getPlayerEntity()
            const y = new SoulReaver(this.engineRef, engine.map.addSprite(15* 16, 17 * 16, p.sprite.layer, 'soulreaver.ika-sprite'))
            this.engineRef.pyAddEntity(y)
            this.engineRef.addMapThing(new DeathListener(this.engineRef, y))
            return true
        } else if (this.engineRef.hasSaveFlag('waterrune') && !this.engineRef.hasSaveFlag('nearend')) {
            const p = this.engineRef.getPlayerEntity()
            this.engineRef.pyAddEntity(
                new Yeti(this.engineRef, engine.map.addSprite(15* 16, 32 * 16, p.sprite.layer, 'yeti.ika-sprite'))
            )
            return true
        }
        return false
    }
}
