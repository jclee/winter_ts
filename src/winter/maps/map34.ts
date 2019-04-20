import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { manaPool, to27, to35, to38 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *manaPool(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.stats.mp += 1
}

export function *to27(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map27.ika-map', [6 * 16, 34 * 16])
}

export function *to35(engineRef: PyEngine) {
    const offset_from = 42 * 16  // first vertical pos possible
    const offset_to = 11 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map35.ika-map', [x, 23 * 16])
}

export function *to38(engineRef: PyEngine) {
    const offset_from = 8 * 16  // first vertical pos possible
    const offset_to = 16 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map38.ika-map', [28 * 16, y])
}
