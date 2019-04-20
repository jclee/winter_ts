import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to2, to4 })

export function autoexec(engineRef: PyEngine) {
    engineRef.addThing(new Snow(engineRef, 5000, [-.5, 2]))
}

export function *to2(engineRef: PyEngine) {
    const offset_from = 6 * 16  // first horizontal pos possible
    const offset_to = 14 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map02.ika-map', [1 * 16, y])
}

export function *to4(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first horizontal pos possible
    const offset_to = 11 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map04.ika-map', [x, 38 * 16])
}
