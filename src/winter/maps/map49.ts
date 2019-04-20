import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to1, to47 })

export function autoexec(_engineRef: PyEngine) {}

export function *to1(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map01.ika-map', [53 * 16, 4.5 * 16])
}

export function *to47(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y
    yield* engineRef.mapSwitchTask('map47.ika-map', [1 * 16, y])
}
