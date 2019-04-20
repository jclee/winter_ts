import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to19, to22, to23, lowerPath, middlePath, upperPath })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to19(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map19.ika-map', [p.sprite.x, 1 * 16])
}

export function *to22(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map22.ika-map', [1 * 16, p.sprite.y])
}

export function *to23(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map23.ika-map', [48 * 16, p.sprite.y])
}

export function *lowerPath(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.sprite.layer = 1
}

export function *middlePath(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.sprite.layer = 3
}

export function *upperPath(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.sprite.layer = 4
}
