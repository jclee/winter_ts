import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to27 })

export function autoexec(_engineRef: PyEngine) {}

export function *to27(engineRef: PyEngine) {
    const offset_from = 13 * 16  // first vertical pos possible
    const offset_to = 33 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map27.ika-map', [x, 1 * 16])
}
