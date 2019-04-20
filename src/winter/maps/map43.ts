import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to2, to44 })

export function autoexec(_engineRef: PyEngine) {}

export function *to2(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map02.ika-map', [48 * 16, p.sprite.y])
}

export function *to44(engineRef: PyEngine) {
    const offset_from = 3 * 16  // first horizontal pos possible
    const offset_to = 22 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map44.ika-map', [1 * 16, y])
}
