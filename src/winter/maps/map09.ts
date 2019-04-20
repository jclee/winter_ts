import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to8, to10 })

export function autoexec(_engineRef: PyEngine) {}

export function *to8(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map08.ika-map', [1 * 16, p.sprite.y])
}

export function *to10(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map10.ika-map', [p.sprite.x, 28 * 16])
}
