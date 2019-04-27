import { Direction } from "./../direction.js"
import { MapScript } from "./mapscript.js"
import { Player } from "./../player.js"
import { Serpent } from "./../serpent.js"
import { PyEngine, random } from "./../winter.js"

export default new MapScript(autoexec, { finalBattle, to31, to33 })

export function autoexec(_engineRef: PyEngine) {}

function *walkUp(p: Player) {
    p.move(Direction.Up, 128)
    p.startAnimation('walk')
    for (let n = 0; n < 128; ++n) {
        yield null
    }
}

// essentially autoexec
export function *finalBattle(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    if (engineRef.hasSaveFlag('finalbattle')) {
        // make the river passable
    } else {
        engineRef.setSaveFlag('finalbattle', 'True')

        const p = engineRef.getPlayerEntity()

        p.setState(walkUp(p))

        for (let n = 0; n < 128; ++n) {
            yield* engineRef.tickTask()
            engineRef.draw()
            engine.video.showPage()
            yield null
        }

        p.startAnimation('stand')
        p.setState(p.noOpState())

        for (let n = 0; n < 256; ++n) {
            // teh earthquake
            engine.map.xwin += random(-4, 5)
            engine.map.ywin += random(-4, 5)
            yield* engineRef.tickTask()
            engineRef.draw()
            engine.video.showPage()
            yield null
        }

        const s = new Serpent(
            engineRef,
            engine.map.addSprite(25 * 16, 24 * 16, p.sprite.layer, 'serpent.ika-sprite')
            )
        s.startAnimation('appear')
        engineRef.addEntity(s)

        for (let n = 19; n < 32; ++n) {
            // close off the way back
            engine.map.setTile(n, 38, p.sprite.layer, 26)
            engine.map.setTile(n, 39, p.sprite.layer, 32)
            engine.map.setObs(n, 38, p.sprite.layer, 1)
            yield* engineRef.tickTask()
            engineRef.draw()
            engine.video.showPage()
            yield null
        }

        p.setState(p.defaultState())

        s.setState(s.roarState())
        engineRef.synchTime()
    }
}

export function *to31(_engineRef: PyEngine): IterableIterator<null> {}
export function *to33(_engineRef: PyEngine): IterableIterator<null> {}
