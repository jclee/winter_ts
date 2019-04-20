import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to46, to48, to49 })

export function autoexec(_engineRef: PyEngine) {}

export function *to46(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map46.ika-map', [25 * 16, 13.5 * 16])
}

export function *to48(engineRef: PyEngine) {
    const offset_from = 81 * 16  // first horizontal pos possible
    const offset_to = 18 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map48.ika-map', [x, 28 * 16])
}

export function *to49(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y
    yield* engineRef.mapSwitchTask('map49.ika-map', [43 * 16, y])
}
