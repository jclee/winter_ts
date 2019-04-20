import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, {to1, to3, to6, to43})

export function autoexec(engineRef: PyEngine) {
    engineRef.addThing(new Snow(engineRef, 3000, [-1, 1.5]))
}

export function *to1(engineRef: PyEngine) {
    const offset_from = 38 * 16  // first vertical pos possible
    const offset_to = 4 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map01.ika-map', [1 * 16, y])
}

export function *to3(engineRef: PyEngine) {
    const offset_from = 14 * 16  // first vertical pos possible
    const offset_to = 6 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map03.ika-map', [98 * 16, y])
}

export function *to6(engineRef: PyEngine) {
    const offset_from = 7 * 16  // first vertical pos possible
    const offset_to = 16 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map06.ika-map', [x, 38 * 16])
}

export function *to43(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map43.ika-map', [1 * 16, p.sprite.y])
}
