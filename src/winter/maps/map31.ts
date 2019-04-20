import { MapScript } from "./mapscript.js"
import { sceneTask } from "./../cabin.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to30, to32 })

export function autoexec(_engineRef: PyEngine) {}

export function *to30(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    const x = p.sprite.x - 160
    yield* engineRef.mapSwitchTask('map30.ika-map', [6 * 16 + x, 16])
    if (!engineRef.hasSaveFlag('nearend')) {
        yield* sceneTask(engineRef, 'nearend')
    }
}

export function *to32(engineRef: PyEngine) {
    // no adjustment here on purpose
    yield* engineRef.mapSwitchTask('map32.ika-map', [25 * 16, 38 * 16])
}
