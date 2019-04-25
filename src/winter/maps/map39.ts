import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to38, to40, to41 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.addMapThing(new Snow(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to38(engineRef: PyEngine) {
    const offset_from = 4 * 16  // first vertical pos possible
    const offset_to = 6 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map38.ika-map', [x, 28 * 16])
}

export function *to40(engineRef: PyEngine) {
    const offset_from = 5 * 16  // first vertical pos possible
    const offset_to = 8 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map40.ika-map', [x, 1 * 16])
}

export function *to41(engineRef: PyEngine) {
    const offset_from = 34 * 16  // first vertical pos possible
    const offset_to = 8 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map41.ika-map', [1 * 16, y])
}
