import { createBlurImages, freeBlurImages } from "./effects.js";
import { AttribWindow, MagicWindow, MenuWindow, StatWindow, Widget } from "./gui.js";
import { Engine, Image, PyEngine, RGB } from "./winter.js";

class Transition {
    private children: WindowMover[] = []

    addChild(
        child: Widget,
        startPos: [number, number] | null = null,
        endPos: [number, number] | null = null,
        time: number
    ) {
        const p = child.getPosition()
        this.children.push(new WindowMover(child, startPos || p, endPos || p, time))
    }

    update(timeDelta: number) {
        const newChildren: WindowMover[] = []
        for (let child of this.children) {
            child.update(timeDelta)

            if (!child.isDone()) {
                newChildren.push(child)
            }
            this.children = newChildren
        }
    }

    draw() {
        for (let child of this.children) {
            child.draw()
        }
    }
}

class WindowMover {
    private time: number = 0
    private delta: [number, number]

    constructor(
        private theWindow: Widget,
        private startPos: [number, number],
        private endPos: [number, number],
        private endTime: number
    ) {
        // change in position that occurs every tick.
        this.delta = [
            (endPos[0] - startPos[0]) / this.endTime,
            (endPos[1] - startPos[1]) / this.endTime
        ]

        // Looks like "window" is special for Brython...
        //this.window.setPosition(startPos)
        this.theWindow.setPosition(startPos)
    }

    isDone() {
        return this.time >= this.endTime
    }

    update(timeDelta: number) {
        if (this.time + timeDelta >= this.endTime) {
            this.time = this.endTime
            this.theWindow.setPosition(this.endPos)
        } else {
            this.time += timeDelta

            // typical interpolation stuff
            // maybe parameterize the algorithm, so that we can have nonlinear movement.
            // Maybe just use a matrix to express the transform.
            this.theWindow.setPosition([
                Math.floor(this.delta[0] * this.time + this.startPos[0]),
                Math.floor(this.delta[1] * this.time + this.startPos[1])
            ])
        }
    }

    draw() {
        this.theWindow.draw()
    }
}

export class PauseScreen {
    private engine: Engine
    private statWnd: StatWindow
    private attribWnd: AttribWindow
    private magWnd: MagicWindow
    private menu: MenuWindow
    private images: Image[] = []

    constructor(
        private engineRef: PyEngine,
    ) {
        this.engine = engineRef.getEngine()
        this.statWnd = new StatWindow(engineRef)
        this.attribWnd = new AttribWindow(engineRef)
        this.magWnd = new MagicWindow(engineRef)
        this.menu = new MenuWindow(engineRef)
    }

    update() {
        this.statWnd.update()
        this.attribWnd.update()
        this.magWnd.update()
        this.statWnd.dockTop().dockLeft()
        this.attribWnd.setPosition([this.statWnd.getX(), this.statWnd.getBottom() + this.statWnd.getBorder() * 2]) // eek
        this.magWnd.setPosition([this.statWnd.getX(), this.attribWnd.getBottom() + this.attribWnd.getBorder() * 2])
        this.menu.dockRight().dockTop()
    }

    *showTask() {
        // assume the backbuffer is already filled
        this.images = createBlurImages(this.engineRef)
        const TIME = 40

        this.update()

        const t = new Transition()
        t.addChild(this.statWnd, [-this.statWnd.getRight(), this.statWnd.getY()], null, TIME - 5)
        t.addChild(this.attribWnd, [-this.attribWnd.getRight(), this.attribWnd.getY()], null, TIME - 5)
        t.addChild(this.magWnd, [-this.magWnd.getRight(), this.magWnd.getY()], null, TIME - 5)
        t.addChild(this.menu, [this.engine.video.xres, this.menu.getY()], null, TIME - 5)

        const startTime = this.engine.getTime()
        let now = startTime
        const endTime = now + TIME
        let prevTime = 0
        while (now < endTime) {
            const time = Math.floor(now - startTime)
            const deltaTime = time - prevTime
            prevTime = time
            if (deltaTime > 0) {
                t.update(deltaTime)
                const o = Math.floor(time * 128 / TIME) // tint intensity for this frame
                const f = Math.floor(time * this.images.length / TIME) // blur image to draw

                this.engine.video.scaleBlit(this.images[f], 0, 0, this.engine.video.xres, this.engine.video.yres)
                this.engine.video.drawRect(0, 0, this.engine.video.xres, this.engine.video.yres, RGB(0, 0, 0, o))
                this.draw()
                this.engine.video.showPage()
            }
            yield null
            now = this.engine.getTime()
        }

        // TODO: Not used, but maybe should be?:
        //this.background = this.images[-1]
    }

    *hideTask() {
        const TIME = 40
        const t = new Transition()
        t.addChild(this.statWnd, null, [-this.statWnd.getRight(), this.statWnd.getY()], TIME - 5)
        t.addChild(this.attribWnd, null, [-this.attribWnd.getRight(), this.attribWnd.getY()], TIME - 5)
        t.addChild(this.magWnd, null, [-this.magWnd.getRight(), this.magWnd.getY()], TIME - 5)
        t.addChild(this.menu, null, [this.engine.video.xres, this.menu.getY()], TIME - 5)

        const startTime = this.engine.getTime()
        let now = startTime
        const endTime = now + TIME
        let prevTime = 0
        while (now < endTime) {
            const time = Math.floor(now - startTime)
            const deltaTime = time - prevTime
            prevTime = time
            if (deltaTime > 0) {
                t.update(deltaTime)
                const o = Math.floor((TIME - time) * 255 / TIME) // menu opacity for this frame
                const f = Math.floor((TIME - time) * this.images.length / TIME) // blur image to draw

                this.engine.video.scaleBlit(this.images[f], 0, 0, this.engine.video.xres, this.engine.video.yres)
                this.engine.video.drawRect(0, 0, this.engine.video.xres, this.engine.video.yres, RGB(0, 0, 0, Math.floor(o / 2)))
                this.draw()
                this.engine.video.showPage()
            }
            yield null
            now = this.engine.getTime()
        }

        //this.background = null
        freeBlurImages(this.engineRef, this.images)
    }

    draw() {
        this.statWnd.draw()
        this.attribWnd.draw()
        this.magWnd.draw()
        this.menu.draw()
    }

    *runTask() {
        yield* this.showTask()
        while (true) {
            this.engine.video.scaleBlit(this.images[this.images.length - 1], 0, 0, this.engine.video.xres, this.engine.video.yres)
            this.engine.video.drawRect(0, 0, this.engine.video.xres, this.engine.video.yres, RGB(0, 0, 0, 128))
            this.draw()
            this.engine.video.showPage()
            yield null

            const result = this.menu.update()
            if (result === 'cancel' || result === 0) {
                break
            } else if (result === 1) {
                yield* this.exitGameTask()
            }
        }

        yield* this.hideTask()
    }

    *exitGameTask(): IterableIterator<null> {
        // TODO: shiny fade out
        this.engineRef.triggerGameQuit()
    }
}
