import { MapScript } from "./mapscript.js"
import { sceneTask } from "./../cabin.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to23, to26, to30 })

export function autoexec(_engineRef: PyEngine) {}

export function *to23(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map23.ika-map', [6 * 16, 42 * 16])
}

export function *to26(engineRef: PyEngine) {
    const offset_from = 50 * 16  // first vertical pos possible
    const offset_to = 20 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map26.ika-map', [38 * 16, y])
}

export function *to30(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map30.ika-map', [9*16, 21*16])
    if (!engineRef.hasSaveFlag('nearend')) {
        yield* sceneTask(engineRef, 'nearend')
    }
}
