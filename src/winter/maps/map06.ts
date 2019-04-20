import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to2, to7, to8 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
    engineRef.addThing(new Snow(engineRef))
}

export function *to2(engineRef: PyEngine) {
    const offset_from = 16 * 16  // first vertical pos possible
    const offset_to = 7 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map02.ika-map', [x, 1 * 16])
}

export function *to7(engineRef: PyEngine) {
    const offset_from = 4 * 16  // first vertical pos possible
    const offset_to = 21 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map07.ika-map', [1 * 16, y])
}

export function *to8(engineRef: PyEngine) {
    const offset_from = 3 * 16  // first vertical pos possible
    const offset_to = 29 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map08.ika-map', [48 * 16, y])
}
