import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to7, to14, to16 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.addMapThing(new Snow(engineRef, 4000, [-1, 1.5]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to7(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map07.ika-map', [78 * 16, p.sprite.y])
}

export function *to14(engineRef: PyEngine) {
    const offset_from = 49 * 16  // first horizontal pos possible
    const offset_to = 6 * 16  // first horizontal pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map14.ika-map', [x, 28 * 16])
}

export function *to16(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map16.ika-map', [1 * 16, p.sprite.y])
}
