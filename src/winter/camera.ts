import { Thing } from "./thing.js"
import { Engine, PyEngine } from "./winter.js"

export class Camera extends Thing {
    public locked: boolean
    private engine: Engine

    constructor(
        private engineRef: PyEngine,
    ) {
        super()
        this.engine = engineRef.getEngine()
        this.locked = false
    }

    update() {
        if (!this.locked) {
            const p = this.engineRef.getPlayerEntity()
            const x = p.sprite.x - Math.floor(this.engine.video.xres / 2)
            const y = p.sprite.y - Math.floor(this.engine.video.yres / 2)

            let ywin = this.engine.map.ywin
            let xwin = this.engine.map.xwin

            if (y > ywin) { ywin += 1 }
            if (y < ywin) { ywin -= 1 }
            if (x > xwin) { xwin += 1 }
            if (x < xwin) { xwin -= 1 }

            this.engine.map.ywin = ywin
            this.engine.map.xwin = xwin
        }
        return false
    }

    center() {
        const p = this.engineRef.getPlayerEntity()
        this.engine.map.xwin = p.sprite.x - Math.floor(this.engine.video.xres / 2)
        this.engine.map.ywin = p.sprite.y - Math.floor(this.engine.video.yres / 2)
    }
}
