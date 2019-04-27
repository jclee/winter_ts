import { MapScript } from "./mapscript.js"
import { FireRune } from "./../rune.js"
import { Thing } from "./../thing.js"
import { PyEngine } from "./../winter.js"
import { SoulReaver, Yeti } from "./../yeti.js"

export default new MapScript(autoexec, { to9 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    if (!engineRef.hasSaveFlag('fireguard')) {
        engineRef.addMapThing(new RuneListener(engineRef))
    }

    if (engineRef.hasSaveFlag('firerune')) {
        engine.map.removeSprite(engine.map.sprites['demiyeti'])
    } else {
        engineRef.addMapThing(new DeathListener(engineRef))
    }
}

export function *to9(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map09.ika-map', [p.sprite.x, 1 * 16])
}

class DeathListener extends Thing {
    // Waits until the yeti is dead, then drops the fire rune.
    constructor(private engineRef: PyEngine, private yeti: Yeti | null = null) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        if (this.yeti === null) {
            // have to get the entity here, since it hasn't been created yet
            // in AutoExec. (if we had more time, I'd fix that problem instead of
            // doing this)
            this.engineRef.playMusic("music/Competative.xm")
            const y = this.engineRef.getEntityForSpriteName(engine.map.sprites['demiyeti'].name)
            if (!(y instanceof Yeti)) { throw new Error("Expected Yeti") }
            this.yeti = y
        } else if (this.yeti.stats.hp === 0) {
            if (!this.engineRef.hasSaveFlag('nearend')) {
                const e = engine.map.addSprite(71, 132, 2, 'firerune.ika-sprite')
                e.name = 'firerune'
                this.engineRef.addEntity(new FireRune(this.engineRef, e))
            } else {
                this.engineRef.playMusic("music/winter.ogg")
                this.engineRef.setSaveFlag('fireguard', 'True')
            }
            return true
        }
        return false
    }
}

class RuneListener extends Thing {
    constructor(private engineRef: PyEngine) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        if (this.engineRef.hasSaveFlag('nearend')) {
            this.engineRef.playMusic('music/resurrection.it')
            const y = new SoulReaver(this.engineRef, engine.map.addSprite(21*16, 13*16, 2, 'soulreaver.ika-sprite'))
            this.engineRef.addEntity(y)
            this.engineRef.addMapThing(new DeathListener(this.engineRef, y))
            return true
        }
        return false
    }
}
