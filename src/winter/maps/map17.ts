import { MapScript } from "./mapscript.js"
import { PyEngine } from "./../winter.js"

export default new MapScript(autoexec, { to16, Tunnel1_1, Tunnel1_2, Tunnel2_1, Tunnel2_2, Around1, Around2 })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
    engine.map.setObs(10,3,3,0)
}

export function *to16(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map16.ika-map', [38 * 16, p.sprite.y])
}

export function *Tunnel1_1(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engine.map.setObs(10,3,3,1)
    engine.map.setObs(16,7,3,0)
    engine.map.setObs(6,14,3,0)
    yield* engineRef.warpTask([16 * 16, 7 * 16])
}

export function *Tunnel1_2(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engine.map.setObs(10,3,3,0)
    engine.map.setObs(16,7,3,1)
    yield* engineRef.warpTask([10 * 16, 3 * 16])
}

export function *Tunnel2_1(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engine.map.setObs(6,14,3,1)
    engine.map.setObs(15,18,3,0)
    yield* engineRef.warpTask([15 * 16, 18 * 16])
}

export function *Tunnel2_2(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engine.map.setObs(6,14,3,0)
    engine.map.setObs(15,18,3,1)
    yield* engineRef.warpTask([6 * 16, 14 * 16])
}

export function *Around1(engineRef: PyEngine) {
    yield* engineRef.warpTask([1.5 * 16, 15 * 16])
}

export function *Around2(engineRef: PyEngine) {
    yield* engineRef.warpTask([18.5 * 16, 18 * 16])
}
