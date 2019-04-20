import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to21, to24, to25, Tunnel1_1, Tunnel1_2, Tunnel2_1, Tunnel2_2, Tunnel3_1, Tunnel3_2, Tunnel4_1, Tunnel4_2, Tunnel5_1, Tunnel5_2, Tunnel6_1, Tunnel6_2, Tunnel7_1, Tunnel7_2 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to21(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map21.ika-map', [1 * 16, p.sprite.y])
}

export function *to24(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map24.ika-map', [48 * 16, 34 * 16])
}

export function *to25(engineRef: PyEngine) {
    yield* engineRef.mapSwitchTask('map25.ika-map', [54 * 16, 55 * 16])
}

export function *Tunnel1_1(engineRef: PyEngine) {
    yield* engineRef.warpTask([21 * 16, 21 * 16])
}

export function *Tunnel1_2(engineRef: PyEngine) {
    yield* engineRef.warpTask([31 * 16, 36 * 16])
}

export function *Tunnel2_1(_engineRef: PyEngine): IterableIterator<null> {}

export function *Tunnel2_2(_engineRef: PyEngine): IterableIterator<null> {}

export function *Tunnel3_1(engineRef: PyEngine) {
    yield* engineRef.warpTask([6 * 16, 16 * 16])
}

export function *Tunnel3_2(engineRef: PyEngine) {
    yield* engineRef.warpTask([22 * 16, 27 * 16])
}

export function *Tunnel4_1(engineRef: PyEngine) {
    yield* engineRef.warpTask([5 * 16, 34 * 16])
}

export function *Tunnel4_2(engineRef: PyEngine) {
    yield* engineRef.warpTask([30 * 16, 8 * 16])
}

export function *Tunnel5_1(engineRef: PyEngine) {
    yield* engineRef.warpTask([18 * 16, 36 * 16])
}

export function *Tunnel5_2(engineRef: PyEngine) {
    yield* engineRef.warpTask([45 * 16, 44 * 16])
}

export function *Tunnel6_1(engineRef: PyEngine) {
    yield* engineRef.warpTask([45 * 16, 37 * 16])
}

export function *Tunnel6_2(engineRef: PyEngine) {
    yield* engineRef.warpTask([6 * 16, 25 * 16])
}

export function *Tunnel7_1(_engineRef: PyEngine): IterableIterator<null> {}

export function *Tunnel7_2(_engineRef: PyEngine): IterableIterator<null> {}
