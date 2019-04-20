import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to47 })

export function autoexec(_engineRef: PyEngine) {}

export function *to47(engineRef: PyEngine) {
    const offset_from = 18 * 16  // first horizontal pos possible
    const offset_to = 81 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map47.ika-map', [x, 1 * 16])
}
