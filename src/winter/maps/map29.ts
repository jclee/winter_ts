import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to27 })

export function autoexec(_engineRef: PyEngine) {}

export function *to27(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first vertical pos possible
    const offset_to = 22 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map27.ika-map', [38 * 16, y])
}
