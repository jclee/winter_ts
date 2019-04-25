import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to35, to37 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.addMapThing(new Snow(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to35(engineRef: PyEngine) {
    const offset_from = 4 * 16  // first vertical pos possible
    const offset_to = 8 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map35.ika-map', [x, 1 * 16])
}

export function *to37(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map37.ika-map', [p.sprite.x, 13 * 16])

}
