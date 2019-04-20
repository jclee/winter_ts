import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to6, to13 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
    engineRef.addThing(new Snow(engineRef))
}

export function *to6(engineRef: PyEngine) {
    const offset_from = 21 * 16  // first vertical pos possible
    const offset_to = 4 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map06.ika-map', [38 * 16, y])
}

export function *to13(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map13.ika-map', [1 * 16, p.sprite.y])
}
