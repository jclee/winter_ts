import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to6, to9, to11, to42 })

export function autoexec(engineRef: PyEngine) {
    engineRef.addMapThing(new Snow(engineRef))
}

export function *to6(engineRef: PyEngine) {
    const offset_from = 29 * 16  // first vertical pos possible
    const offset_to = 3 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map06.ika-map', [1 * 16, y])
}

export function *to9(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map09.ika-map', [28 * 16, p.sprite.y])
}

export function *to11(engineRef: PyEngine) {
    const offset_from = 23 * 16  // first vertical pos possible
    const offset_to = 21 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map11.ika-map', [x, 1 * 16])
}

export function *to42(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map42.ika-map', [p.sprite.x, 28 * 16])
}
