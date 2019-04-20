import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to11 })

export function autoexec(_engineRef: PyEngine) {}

export function *to11(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map11.ika-map', [23 * 16, 17 * 16])
}
