import { Thing } from "./thing.js"
import { Engine, Image, PyEngine } from "./winter.js"

const sgn = (i: number) => {
    if (i > 0) { return 1 }
    if (i < 0) { return -1 }
    return 0
}

class Gauge extends Thing {
    protected engine: Engine
    protected engineRef: PyEngine
    protected span: Image
    protected left: Image
    protected middle: Image
    protected right: Image
    protected oldVal: number
    protected oldMax: number
    protected x: number
    protected y: number
    protected opacity: number
    protected rgb: [number, number, number]
    protected fadeIn: boolean

    constructor(
        engineRef: PyEngine,
        imageNames: [string, string, string, string],
    ) {
        super()
        // imageName - name of the image series to use.
        //  ie 'gfx/ui/barhp%i.png'

        this.engine = engineRef.getEngine()
        this.engineRef = engineRef
        const images = imageNames.map(n => this.engine.getImage(n))
        ;[this.span, this.left, this.middle, this.right] = images
        this.oldVal = 0
        this.oldMax = 0
        this.x = 0
        this.y = 0
        this.opacity = 0
        this.rgb = [255, 255, 255]
        this.fadeIn = false
    }

    curVal() { return 0 }
    curMax() { return 0 }

    update() {
        const v = sgn(this.curVal() - this.oldVal)
        const m = sgn(this.curMax() - this.oldMax)

        if (this.fadeIn) {
            this.opacity = Math.min(512, this.opacity + 20)
            if (this.opacity === 512) {
                this.fadeIn = false
            }
        }

        if (v === 0 && m === 0) {
            this.opacity = Math.max(0, this.opacity - 1)
        } else {
            this.fadeIn = true
            this.oldVal += v
            this.oldMax += m
        }
        return false
    }

    draw() {
        if (this.opacity === 0) {
            return
        }

        const o = Math.min(1.0, this.opacity / 255.0)

        // the width of the repeated span image thingo.
        // each end of the gauge occupies two pixels, so we subtract four.
        // (bad hack, I know)
        const width = this.oldMax - 3

        let x = this.engine.video.xres - width - this.left.width - this.right.width - this.x - 2

        this.engine.video.tintBlit(this.left, x, this.y, o)
        this.engine.video.tintBlit(this.right, x + width + this.left.width, this.y, o)

        x += this.left.width

        this.engine.video.tintScaleBlit(this.span, x, this.y, width, this.span.height, o)

        x -= 2

        let v: number= this.oldVal

        if (this.oldVal) {
            this.drawRect(x + this.oldMax - v, this.y + 5, x + this.oldMax, this.y + 6, o)
        }
    }

    drawRect(x: number, y: number, w: number, h: number, opacity: number) {
        // Used to draw in the filled part of the gauge.
        this.engine.video.drawRect(x, y, w, h, this.rgb[0], this.rgb[1], this.rgb[2], opacity)
    }
}

export class HPBar extends Gauge {
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef, [
            'gfx/ui/barhp0.png',
            'gfx/ui/barhp1.png',
            'gfx/ui/barhp2.png',
            'gfx/ui/barhp3.png',
        ])
        this.y = this.engine.video.yres - this.left.height - 1
        this.rgb = [1, 0, 0]
    }

    curVal() { return this.engineRef.getPlayerEntity().stats.hp }
    curMax() { return this.engineRef.getPlayerEntity().stats.maxhp }
}

export class MPBar extends Gauge {
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef, [
            'gfx/ui/barhp0.png',
            'gfx/ui/barhp1.png',
            'gfx/ui/barhp2.png',
            'gfx/ui/barhp3.png',
        ])
        this.y = this.engine.video.yres - this.left.height * 2 - 1
        this.rgb = [0, 0, 1]
        this.oldMax = this.curMax()
        this.oldVal = this.curVal()
    }

    curVal() { return this.engineRef.getPlayerEntity().stats.mp }
    curMax() { return this.engineRef.getPlayerEntity().stats.maxmp }
}

export class EXPBar extends Gauge {
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef, [
            'gfx/ui/barmp0.png',
            'gfx/ui/barmp1.png',
            'gfx/ui/barmp2.png',
            'gfx/ui/barmp3.png',
        ])
        //this.y = this.engine.video.yres - this.left.height * 2 - 1
        this.rgb = [0, 0.5, 0.5]
        this.oldMax = this.curMax()
        this.oldVal = this.curVal()
    }

    drawRect(x: number, y: number, w: number, h: number, opacity: number) {
        super.drawRect(x, y, w, h - 1, opacity)
    }

    curVal() { return Math.floor(this.engineRef.getPlayerEntity().stats.exp * 100 / this.engineRef.getPlayerEntity().stats.next) }
    curMax() { return 100 }
}
