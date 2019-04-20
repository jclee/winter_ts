import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to34, to36 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to34(engineRef: PyEngine) {
    const offset_from = 11 * 16  // first vertical pos possible
    const offset_to = 42 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map34.ika-map', [x, 1 * 16])
}

export function *to36(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first vertical pos possible
    const offset_to = 4 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map36.ika-map', [x, 38 * 16])
}
