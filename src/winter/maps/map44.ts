import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to43, to45, to46 })

export function autoexec(_engineRef: PyEngine) {}

export function *to43(engineRef: PyEngine) {
    const offset_from = 22 * 16  // first horizontal pos possible
    const offset_to = 3 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map43.ika-map', [58 * 16, y])
}

export function *to45(engineRef: PyEngine) {
    const offset_from = 28 * 16  // first horizontal pos possible
    const offset_to = 23 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map45.ika-map', [x, 1 * 16])
}

export function *to46(engineRef: PyEngine) {
    const offset_from = 32 * 16  // first horizontal pos possible
    const offset_to = 6 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map46.ika-map', [1 * 16, y])
}
