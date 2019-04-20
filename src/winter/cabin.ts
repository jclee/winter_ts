import { fadeInTask, fadeOutTask } from "./effects.js"
import { Entity } from "./entity.js"
import { ScrollableTextFrame } from "./gui.js"
import { delayTask, PyEngine, RGB, Sprite } from "./winter.js"
import { wrapText } from "./wraptext.js"

class Tinter {
    private curTint = 0
    public tint = 0

    draw(engineRef: PyEngine) {
        const engine = engineRef.getEngine()

        this.curTint += (this.curTint < this.tint) ? 1 : 0
        this.curTint -= (this.curTint > this.tint) ? 1 : 0

        if (this.curTint) {
            engine.video.DrawRect(0, 0, engine.video.xres, engine.video.yres, RGB(0, 0, 0, this.curTint))
        }
    }
}

const tint = new Tinter()

let crap: ScrollableTextFrame[] = [] // crap to draw along with the map

function draw(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    engine.map.Render()
    tint.draw(engineRef)
    for (let c of crap) {
        c.draw()
    }
}

//------------------------------------------------------------------------------

function textBox(engineRef: PyEngine, sprite: Sprite, txt: string) {
    const engine = engineRef.getEngine()
    const WIDTH = 200
    let width = WIDTH
    const font = engineRef.font
    let text = wrapText(txt, width, font)
    width = Math.max(...text.map(s => font.StringWidth(s)))
    let height = text.length * font.height

    let x = sprite.x + Math.floor(sprite.hotwidth / 2) - engine.map.xwin
    let y = sprite.y - engine.map.ywin

    if (x < Math.floor(engine.video.xres / 2)) {
        x -= Math.floor(width / 2)
    }

    width = WIDTH
    if (x + width + 16 > engine.video.xres) {
        text = wrapText(txt, engine.video.xres - x - 16, font)
        width = Math.max(...text.map(s => font.StringWidth(s)))
        height = text.length * font.height
    }

    const frame = new ScrollableTextFrame(engineRef)
    frame.addText(text)
    frame.autoSize()

    if (y > Math.floor(engine.video.yres / 2)) {
        y += 32
    } else {
        y -= frame.getHeight() + 16
    }

    frame.setPosition([x, y])
    return frame
}

//------------------------------------------------------------------------------

function *speech(engineRef: PyEngine, where: Sprite, txt: string) {
    // Displays a text frame.
    const engine = engineRef.getEngine()
    const frame = textBox(engineRef, where, txt)

    while (!engine.controls.attack()) {
        draw(engineRef)
        frame.draw()
        engine.video.ShowPage()
        yield null
    }
}

//------------------------------------------------------------------------------

function *animateHelper(engineRef: PyEngine, sprite: Sprite, frames: number[], delay: number, loop: boolean) {
    const engine = engineRef.getEngine()
    while (true) {
        for (let frame of frames) {
            sprite.specframe = frame
            let d = delay
            while (d > 0) {
                d -= 1
                draw(engineRef)
                engine.video.ShowPage()
                yield* delayTask(1)
                if (engine.controls.attack()) {
                    return
                }
            }
        }
        if (!loop) {
            return
        }
    }
}

function *animate(engineRef: PyEngine, sprite: Sprite, frames: number[], delay: number, text: string | null = null) {
    // frames should be a list of (frame, delay) pairs.
    if (text !== null) {
        crap = [textBox(engineRef, sprite, text)]
    }

    yield* animateHelper(engineRef, sprite, frames, delay, true)

    crap = []
    sprite.specframe = 0
}

//------------------------------------------------------------------------------
// Scene code
//------------------------------------------------------------------------------

const _scenes: {[key: string]: (engineRef: PyEngine) => IterableIterator<null>} = {}

let grandpa: Sprite
let kid1: Sprite
let kid2: Sprite
let kid3: Sprite

// TODO: transitions
export function *sceneTask(engineRef: PyEngine, name: string) {
    const engine = engineRef.getEngine()
    const entities = engineRef.getEntities()
    const getSpritePos: (e: Entity) => [number, number] = e => [e.sprite.x, e.sprite.y]
    const savedPos: [number, number][] = entities.map(getSpritePos)
    // hide 'em all
    for (let e of entities) {
        ;[e.sprite.x, e.sprite.y] = [-100, -100]
    }

    engine.map.Switch('maps/cabinmap.ika-map')
    grandpa = engine.map.sprites['grandpa']
    kid1 = engine.map.sprites['kid1']
    kid2 = engine.map.sprites['kid2']
    kid3 = engine.map.sprites['kid3']

    const draw = () => {
        engine.map.Render()
    }
    yield* fadeInTask(engineRef, 100, draw)

    yield* _scenes[name](engineRef)
    engineRef.setSaveFlag(name, 'True')

    yield* fadeOutTask(engineRef, 100, draw)

    //grandpa = null
    //kid1 = null
    //kid2 = null
    //kid3 = null

    if (engineRef.getMapName()) {
        // We now only call autoexec in engine.mapSwitchTask, not
        // engineRef.map.Switch, so this should be an OK way to restore the map.
        engine.map.Switch('maps/' + engineRef.getMapName())
        for (let i = 0; i < entities.length; ++i) {
            const e = entities[i]
            ;[e.sprite.x, e.sprite.y] = savedPos[i]
        }
    }
}

//------------------------------------------------------------------------------
// Ear's functions
//------------------------------------------------------------------------------

const PAUSE = 0
const SPEAKING = 1
const NOD = 2

const TALKING = [
    ...Array(3).fill(PAUSE),
    ...Array(2).fill(SPEAKING),
    ...Array(3).fill(PAUSE),
    ...Array(2).fill(SPEAKING),
    ...Array(2).fill(PAUSE),
    NOD
]

function *narration(engineRef: PyEngine, text: string) {
    yield* animate(engineRef, grandpa, TALKING, 25, text)
}

//------------------------------------------------------------------------------
// Scenes
//------------------------------------------------------------------------------

function *intro(engineRef: PyEngine) {
    yield* speech(engineRef, kid1, 'Tell us a story!')
    yield* animate(engineRef, kid2, [1], 10, 'Yeah, the one about the ice man!')
    yield* animate(engineRef, kid3, [0, 1], 20, "Yeah!!")
    yield* speech(engineRef, grandpa, "Isn't that story a little scary?")
    yield* speech(engineRef, kid1, 'No!')
    yield* speech(engineRef, kid2, 'Please tell us!')
    yield* speech(engineRef, grandpa, 'Oh all right.  Ahem.')
    yield* animate(engineRef, kid3, [0, 1], 20, "I'm scared!!")

    tint.tint = 200

    yield* narration(engineRef, `
Across the frozen hills of Kuladriat, hunters pursue a man like any other 
prey.  Ever-northward their prey runs, till at last, at the foot of Mount 
Durinar, a chasm of ice confronts him.`.replace('\n', ''))

    yield* narration(engineRef, `
The crack of a bow sounds across the vale; an instant later its arrow burying 
itself in the leg of the hunted man.  His legs buckle beneath him, and he 
tumbles down the cold ravine--`.replace('\n', ''))

    yield* narration(engineRef, "--the sound of stone 'gainst stone resounding.")
    
    tint.tint = 0

    yield* narration(engineRef, `
A sharp whistle signifies the hunt's end.  The hunters will not bother 
to claim their prize, for it is far too cold--his fate is come.`.replace('\n', ''))
}

function *nearend(engineRef: PyEngine) {
    tint.tint = 200
    
    yield* narration(engineRef, `
As he neared his journey's end, he grew tired, and cold, and hungry.`.replace('\n', ''))

    yield* narration(engineRef, `He was willing to do anything to make such neverending 
misery cease, once and for all.`.replace('\n', ''))

    yield* narration(engineRef, `
He considered... going back from whence he came, then.`.replace('\n', ''))

    yield* narration(engineRef, `But, if he were to do so, he would then have to face the 
same trials which had taken such a weary toll on his spirit to begin with.`.replace('\n', ''))

    tint.tint = 0
    
    yield* speech(engineRef, kid1, 'Did he go back?')
    yield* speech(engineRef, kid2, 'Yeah!')
    yield* speech(engineRef, kid3, "No way! He's way too brave!! Yeah!!")
    
    yield* narration(engineRef, `
In the end, no one knows whether he attempted to return... all that is important 
is the outcome.`.replace('\n', ''))

    yield* narration(engineRef, `But should he have gone back, he would have found the greatest reward 
of all.  Not peace... and not relief... but courage.  The courage to continue again.`.replace('\n', ''))
}

//------------------------------------------------------------------------------
// Setup
//------------------------------------------------------------------------------

_scenes['intro'] = intro
_scenes['nearend'] = nearend
