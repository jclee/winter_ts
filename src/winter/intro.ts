import { delayTask, Engine, PyEngine, RGB, Snow } from "./winter.js";

class DoneException {}

function *showTask(engine: Engine, draw: ()=>void, count: number, snowObj: Snow) {
    for (let i = 0; i < count; ++i) {
        draw()
        snowObj.update()
        snowObj.draw()
        engine.video.ShowPage()
        yield *delayTask(1)

        if (engine.controls.attack()) {
            throw new DoneException()
        }
    }
}

export function *introTask(engineRef: PyEngine) {
    const engine = engineRef.getEngine().js
    const snowObj = new Snow(engine, 100, [0, 0.5])
    const gba = engine.getImage('gfx/gba.png')
    const yourmom = engine.getImage('gfx/yourmother.png')
    const isabitch = engine.getImage('gfx/isabigfatbitch.png')

    engine.controls.attack() // unpress

    const v = engine.video
    const d = 40

    const showGba = () => {
        v.ClearScreen()
        v.Blit(
            gba,
            Math.floor((v.xres - gba.width) / 2),
            Math.floor((v.yres - gba.height) / 2)
        )
    }

    try {
        yield *showTask(engine, showGba, 300, snowObj)

        yield *showTask(engine, ()=>{v.ClearScreen()}, d, snowObj)

        for (let i = 0; i < 3; ++i) {
            yield *showTask(engine, ()=>{v.Blit(yourmom, 0, 0)}, d, snowObj)
            yield *showTask(engine, ()=>{v.ClearScreen()}, d, snowObj)
        }

        yield *showTask(engine, ()=>{v.Blit(isabitch, 0, 0)}, Math.floor(d / 2), snowObj)
        yield *showTask(engine, ()=>{v.ClearScreen()}, d, snowObj)
    } catch (e) {
        if (!(e instanceof DoneException)) {
            throw e;
        }
    }
}

export function *menuTask(engineRef: PyEngine, setResult: (r: number)=>void) {
    const engine = engineRef.getEngine().js
    const bg = engine.getImage('gfx/title.png')
    const cursor = engine.getImage('gfx/ui/pointer.png')
    const snowObj = new Snow(engine, 100, [0, 0.5])
    snowObj.update()
    let result: number | null = null
    let cursorPos = 0
    const FADE_TIME = 60

    function draw() {
        engine.video.Blit(bg, 0, 0)
        engine.video.Blit(cursor, 68, 128 + cursorPos * 26)
    }

    for (let i = FADE_TIME - 1; i > -1; --i) {
        draw()
        engine.video.DrawRect(0, 0, engine.video.xres, engine.video.yres, RGB(0, 0, 0, Math.floor(i * 255 / FADE_TIME)))
        snowObj.update()
        snowObj.draw()
        engine.video.ShowPage()
        yield* delayTask(1)
    }

    let u = 0 // gay unpress hack

    while (result === null) {
        draw()
        snowObj.update()
        snowObj.draw()
        engine.video.ShowPage()
        yield* delayTask(1)

        if (engine.controls.up() && cursorPos > 0) {
            if (u === 0) {
                cursorPos -= 1
                u = 1
            }
        } else if (engine.controls.down() && cursorPos < 2) {
            if (u === 0) {
                cursorPos += 1
                u = 1
            }
        } else if (engine.controls.attack()) {
            result = cursorPos
        } else {
            u = 0
        }
    }

    // one last draw.  Later on, there's a blurfade that can take advantage of this:
    draw()
    snowObj.draw()
    setResult(result)
}
