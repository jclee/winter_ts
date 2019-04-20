import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to21, to50 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to21(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map21.ika-map', [38 * 16, p.sprite.y])
}

export function *to50(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map50.ika-map', [9 * 16, 13 * 16])
}
