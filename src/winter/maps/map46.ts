import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to44, to47 })

export function autoexec(_engineRef: PyEngine) {}

export function *to44(engineRef: PyEngine) {
    const offset_from = 6 * 16  // first horizontal pos possible
    const offset_to = 32 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map44.ika-map', [63 * 16, y])
}

export function *to47(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map47.ika-map', [38 * 16, 3.5 * 16])
}
