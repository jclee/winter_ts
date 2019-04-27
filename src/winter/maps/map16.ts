import { MapScript } from "./mapscript.js"
import { WindRune } from "./../rune.js"
import { Thing } from "./../thing.js"
import { delayTask, PyEngine } from "./../winter.js"
import { SoulReaver, Yeti } from "./../yeti.js"

export default new MapScript(autoexec, { bridge_break, manaPool, to13, to17, to19, toLowerLayer, toUpperLayer })

export function autoexec(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engineRef.pySetBackground(engine.getImage('gfx/mountains.png'))

    if (!engineRef.hasSaveFlag('bridge_broken')) {
        for (let x = 19; x < 22; ++x) {
            engine.map.setTile(x, 28, 3, 152)
            engine.map.setTile(x, 29, 3, 158)
            engine.map.setTile(x, 30, 3, 164)
            engine.map.sprites['break_gap'].x = -100
        }
    }

    if (!engineRef.hasSaveFlag('windguard') && engineRef.hasSaveFlag('nearend')) {
        engineRef.addMapThing(new RuneListener(engineRef))
    }
}

export function *bridge_break(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    if (!engineRef.hasSaveFlag('bridge_broken')) {
        engineRef.playMusic('music/Competative.xm')
        engineRef.setSaveFlag('bridge_broken', 'True')

        const bridge = [
            [366, 0, 367],
            [372, 0, 373],
            [378, 0, 379],
        ]

        for (let x = 0; x < 3; ++x) {
            engine.map.setTile(x + 19, 28, 3, bridge[0][x])
            engine.map.setTile(x + 19, 29, 3, bridge[1][x])
            engine.map.setTile(x + 19, 30, 3, bridge[2][x])
            engine.map.sprites['break_gap'].x = 320
        }

        // This is really cheap.  Probably fragile too.  I'm stepping beyond
        // the game engine and directly twiddling with ika.

        const p = engineRef.getPlayerEntity()
        p.stop()
        p.sprite.layer = 2
        p.sprite.specframe = 91
        p.setState(p.noOpState()) // keep the player from moving

        engineRef.draw()
        engine.video.showPage()
        yield* delayTask(8)

        for (let y = 0; y < 32; ++y) {
            p.sprite.y += 1
            engine.map.processSprites()
            engineRef.pyUpdateCamera()
            engineRef.draw()
            engine.video.showPage()
            yield* delayTask(1)
        }

        p.sprite.layer = 1

        for (let y = 0; y < 32; ++y) {
            p.sprite.y += 1
            engine.map.processSprites()
            engineRef.pyUpdateCamera()
            engineRef.draw()
            engine.video.showPage()
            yield* delayTask(1)
        }

        p.sprite.specframe = 92
        const t = engine.getTime() + 80
        while (t > engine.getTime()) {
            engineRef.draw()
            engine.video.showPage()
            yield null
        }

        p.setState(p.standState())

        const y = new Yeti(engineRef, engine.map.addSprite(304, 64, 1, 'yeti.ika-sprite'))
        // UBER-YETI
        y.stats.maxhp = 400
        y.stats.hp = y.stats.maxhp
        y.stats.att += 10
        engineRef.addEntity(y)
        engineRef.addMapThing(new DeathListener(engineRef, y))

        engineRef.synchTime()
    }
}

export function *manaPool(engineRef: PyEngine): IterableIterator<null> {
    if (engineRef.hasSaveFlag('windrune') && (!engineRef.hasSaveFlag('nearend') || engineRef.hasSaveFlag('windguard'))) {
        const p = engineRef.getPlayerEntity()
        p.stats.mp += 1
    }
}

export function *to13(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map13.ika-map', [78 * 16, p.sprite.y])
}

export function *to17(engineRef: PyEngine) {
    const p = engineRef.getPlayerEntity()
    yield* engineRef.mapSwitchTask('map17.ika-map', [1 * 16, p.sprite.y])
}

export function *to19(engineRef: PyEngine) {
    const offset_from = 4 * 16  // first vertical pos possible
    const offset_to = 44 * 16  // first vertical pos possible
    const p = engineRef.getPlayerEntity()
    const y = p.sprite.y - offset_from + offset_to
    yield* engineRef.mapSwitchTask('map19.ika-map', [48 * 16, y])
}

export function *toLowerLayer(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.sprite.layer = 1
}

export function *toUpperLayer(engineRef: PyEngine): IterableIterator<null> {
    const p = engineRef.getPlayerEntity()
    p.sprite.layer = 3
}

class DeathListener extends Thing {
    // Waits until the yeti is dead, then drops the wind rune.
    constructor(private engineRef: PyEngine, private yeti: Yeti) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        if (this.yeti.stats.hp === 0) {
            if (!this.engineRef.hasSaveFlag('windrune')) {
                const e = engine.map.addSprite(304, 304, 1, 'windrune.ika-sprite')
                e.name = 'windrune'
                this.engineRef.addEntity(new WindRune(this.engineRef, e))
            } else {
                this.engineRef.setSaveFlag('windguard', 'True')
            }

            this.engineRef.playMusic('music/winter.ogg')
            return true
        }
        return false
    }
}

class RuneListener extends Thing {
    constructor(private engineRef: PyEngine) { super() }

    update() {
        const engine = this.engineRef.getEngine()
        if (this.engineRef.hasSaveFlag('nearend')) {
            this.engineRef.playMusic('music/resurrection.it')
            const y = new SoulReaver(this.engineRef, engine.map.addSprite(19*16, 20*16, 1, 'soulreaver.ika-sprite'))
            this.engineRef.addEntity(y)
            this.engineRef.addMapThing(new DeathListener(this.engineRef, y))
            return true
        }
        return false
    }
}
