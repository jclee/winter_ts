import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to44 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to44(engineRef: PyEngine) {
    const offset_from = 23 * 16  // first horizontal pos possible
    const offset_to = 28 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map44.ika-map', [x, 48 * 16]) 
}
