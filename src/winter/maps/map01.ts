import { MapScript } from "./mapscript.js"
import { Thing } from "./../thing.js"
import { PyEngine, Snow } from "./../winter.js"
import { Yeti } from "./../yeti.js"

export default new MapScript(autoexec, {to2, to49})

class RuneListener extends Thing {
    constructor(private engineRef: PyEngine) { super() }

    update() {
        if (this.engineRef.getSaveFlag('waterguard') === '') { return false; }
        if (this.engineRef.getSaveFlag('fireguard') === '') { return false; }
        if (this.engineRef.getSaveFlag('windguard') === '') { return false; }

        const engine = this.engineRef.getEngine()
        const p = this.engineRef.getPlayerEntity()
        this.engineRef.pyAddEntity(
            new Yeti(this.engineRef, engine.map.addSprite(35 * 16, 19 * 16, p.sprite.layer, 'yeti.ika-sprite'))
        )
        return true
    }
}

function autoexec(engineRef: PyEngine) {
    engineRef.addMapThing(new Snow(engineRef))
    if (engineRef.getSaveFlag('cowardrune') === '') {
        engineRef.addMapThing(new RuneListener(engineRef))
    }
}

function *to2(engineRef: PyEngine) {
    const offset_from = 4 * 16  // first vertical pos possible
    const offset_to = 38 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map02.ika-map', [48 * 16, y])
}

function *to49(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map49.ika-map', [14 * 16, 23 * 16])
}
