import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to25, to31 })

export function autoexec(_engineRef: PyEngine) {}

export function *to25(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map25.ika-map', [39 * 16, 5 * 16])
}

export function *to31(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x + 16
    yield* engineRef.mapSwitchTask('map31.ika-map', [x, 28 * 16])
}
