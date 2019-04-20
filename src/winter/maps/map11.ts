import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to8, to12 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to8(engineRef: PyEngine) {
    const offset_from = 21 * 16  // first horizontal pos possible
    const offset_to = 23 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map08.ika-map', [x, 38 * 16])
}

export function *to12(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map12.ika-map', [10 * 16, 18 * 16])
}
