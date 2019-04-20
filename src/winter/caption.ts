import { Thing } from "./thing.js"
import { Engine, FontClass, PyEngine } from "./winter.js"

export class Caption extends Thing {
    private x: number
    private y: number
    private opacity: number
    private updateGen: IterableIterator<boolean>

    constructor(
        engineRef: PyEngine,
        private font: FontClass,
        private text: string,
        x: number | null = null,
        y: number | null = null,
        private duration: number = 200,
    ) {
        super()
        const engine: Engine = engineRef.getEngine()

        const width = this.font.StringWidth(text)
        const height = this.font.height

        this.x = (x !== null) ? x : Math.floor((engine.video.xres - width) / 2)
        this.y = (y !== null) ? y : engine.video.yres - height - 40

        this.opacity = 0
        this.updateGen =  this._update()
    }

    private *_update() {
        while (this.opacity < 256) {
            this.opacity += 2
            yield false
        }

        while (this.duration > 0) {
            this.duration -= 1
            yield false
        }

        while (this.opacity > 0) {
            this.opacity -= 2
            yield false
        }

        yield true // seppuku
    }

    update() {
        const { value } = this.updateGen.next()
        return value
    }

    draw() {
        const o = Math.min(255, this.opacity)
        this.font.PrintWithOpacity(this.x, this.y, this.text, o)
    }
}
