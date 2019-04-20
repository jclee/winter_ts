import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to4, to13 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to4(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first horizontal pos possible
    const offset_to = 11 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map04.ika-map', [x, 38 * 16])
}

export function *to13(engineRef: PyEngine) {
    const offset_from = 6 * 16  // first horizontal pos possible
    const offset_to = 49 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map13.ika-map', [x, 1 * 16])
}
