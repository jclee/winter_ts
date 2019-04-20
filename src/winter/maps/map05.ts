import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to4 })

export function autoexec(_engineRef: PyEngine) {}

export function *to4(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map04.ika-map', [15 * 16, 3.5 * 16])
}
