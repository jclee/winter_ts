import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to22 })

export function autoexec(_engineRef: PyEngine) {}

export function *to22(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map22.ika-map', [7 * 16, 11.5 * 16])
}
