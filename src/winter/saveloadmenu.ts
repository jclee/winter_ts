import { fadeInTask, fadeOutTask } from "./effects.js";
import { TextFrame, SaveLoadMenu } from "./gui.js";
import { PyEngine } from "./winter.js"
import { SaveData } from "./saveload.js"

export function *loadMenuTask(
    engineRef: PyEngine,
    setResult: (s: SaveData | null) => void
) {
    const engine = engineRef.getEngine()
    const title = new TextFrame(engineRef, ['Load Game'])
    title.setPosition([16, 16])
    const saves = engineRef.readSaves()
    const m = new SaveLoadMenu(engineRef, saves, false)

    const draw = () => {
        engine.video.ClearScreen() // fix this
        m.draw()
        title.draw()
    }

    yield* fadeInTask(engineRef, 50, draw)

    let i: number | string | null = null
    while (i === null) {
        i = m.update()
        draw()
        engine.video.ShowPage()
        yield null
    }

    draw()
    // Hack to get around brython's lack of support for returning values through
    // "yield from":
    if (i === 'cancel' || i >= saves.length) {
        setResult(null)
    } else {
        // TODO: Better way?
        setResult(saves[(i as number)])
    }
}

export function *saveMenuTask(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    const title = new TextFrame(engineRef, ['Save Game'])
    title.setPosition([16, 16])
    const saves = engineRef.readSaves()
    const m = new SaveLoadMenu(engineRef, saves, true)

    const draw = () => {
        engine.video.ClearScreen() // fix this
        m.draw()
        title.draw()
    }

    yield* fadeInTask(engineRef, 50, draw)

    let i: number | string | null = null
    while (i === null) {
        i = m.update()
        draw()
        engine.video.ShowPage()
        yield null
    }

    if (i !== 'cancel') {
        // TODO: Better way?
        engineRef.writeSave((i as number))
    }

    yield* fadeOutTask(engineRef, 50, draw)
}
