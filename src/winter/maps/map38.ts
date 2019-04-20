import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to34, to39 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.addThing(new Snow(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to34(engineRef: PyEngine) {
    const offset_from = 16 * 16  // first vertical pos possible
    const offset_to = 8 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map34.ika-map', [1 * 16, y])
}

export function *to39(engineRef: PyEngine) {
    const offset_from = 6 * 16  // first vertical pos possible
    const offset_to = 4 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map39.ika-map', [x, 1 * 16])
}
