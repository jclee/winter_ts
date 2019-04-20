import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to8, to41 })

export function autoexec(_engineRef: PyEngine) {}

export function *to8(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map08.ika-map', [p.sprite.x, 1 * 16])
}

export function *to41(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map41.ika-map', [p.sprite.x + 16, 38 * 16])
}
