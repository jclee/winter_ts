import { Carnivore } from "./../anklebiter.js"
import { MapScript } from "./mapscript.js"
import { PyEngine, Snow } from "./../winter.js"

export default new MapScript(autoexec, { to36, releaseAnklebiters })

let spawned = false

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    spawned = false
    engineRef.addMapThing(new Snow(engineRef, 100, [.4, 1], [255,192,255]))
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))
}

export function *to36(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map36.ika-map', [p.sprite.x, 1 * 16])
}

export function *releaseAnklebiters(engineRef: PyEngine): IterableIterator<null> {
    const engine = engineRef.getEngine()

    if (!engineRef.hasSaveFlag('dynamite3') && !spawned) {

        const indeces = [[6,6], [9,6], [12,6], [4, 8], [14, 8], [2, 10], [6, 10], [12, 10], [16, 10], [4,11], [14, 11]]

        for (let i of indeces) {
            engineRef.pyAddEntity(new Carnivore(engineRef, engine.map.addSprite(i[0]*16+8, i[1]*16, 1, "carnivore.ika-sprite")))
        }

        spawned = true
    }
}
