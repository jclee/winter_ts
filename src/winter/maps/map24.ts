import { MapScript } from "./mapscript.js"
import { CowardRune } from "./../rune.js"
import { Thing } from "./../thing.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to23, to50 })

export function autoexec(engineRef: PyEngine) {
    if (engineRef.hasSaveFlag('waterguard')
        && engineRef.hasSaveFlag('windguard')
        && engineRef.hasSaveFlag('fireguard')
    ) {
        engineRef.addThing(new AddRune(engineRef))
    }
}

export function *to23(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map23.ika-map', [5 * 16, 5 * 16])
}

export function *to50(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map50.ika-map', [9 * 16, 13 * 16])
}

class AddRune extends Thing {
    constructor(private engineRef: PyEngine) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        const e = engine.map.addSprite(315, 320, 1, 'cowardrune.ika-sprite')
        e.name = 'cowardrune'
        this.engineRef.pyAddEntity(new CowardRune(this.engineRef, e))
        return true
    }
}
