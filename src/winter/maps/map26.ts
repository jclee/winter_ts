import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to25, to27 })

export function autoexec(_engineRef: PyEngine) {}

export function *to25(engineRef: PyEngine) {
    const offset_from = 20 * 16  // first vertical pos possible
    const offset_to = 50 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map25.ika-map', [1 * 16, y])
}

export function *to27(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map27.ika-map', [p.sprite.x, 78 * 16])
}
