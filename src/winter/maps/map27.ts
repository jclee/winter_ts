import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to26, to28, to29, to34 })

export function autoexec(_engineRef: PyEngine) {}

export function *to26(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map26.ika-map', [p.sprite.x, 1 * 16])
}

export function *to28(engineRef: PyEngine) {
    const offset_from = 33 * 16  // first vertical pos possible
    const offset_to = 13 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map28.ika-map', [x, 28 * 16])
}

export function *to29(engineRef: PyEngine) {
    const offset_from = 22 * 16  // first vertical pos possible
    const offset_to = 8 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map29.ika-map', [1 * 16, y])
}

export function *to34(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map34.ika-map', [74 * 16, 6.5 * 16])
}
