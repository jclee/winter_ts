import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to39, to42 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.addThing(new Snow(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to39(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first vertical pos possible
    const offset_to = 34 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map39.ika-map', [38 * 16, y])
}

export function *to42(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map42.ika-map', [p.sprite.x - 16, 1 * 16])
}
