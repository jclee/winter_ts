interface FlakeState {
    x: number
    y: number
    vx: number
    life: number
}

export class WinterSnow {
    private static readonly MaxLife = 50

    private colorPrefix: string
    private flakes: FlakeState[]
    private yRange: number

    constructor(
        readonly xres: number,
        readonly yres: number,
        readonly count: number,
        readonly velocity: [number, number],
        colorValue: number,
    ) {
        this.flakes = []
        for (let i = 0; i < this.count; ++i) {
            this.flakes.push({x: 0, y: 0, vx: 0, life: 0})
        }
        const r = colorValue & 0xff
        const g = (colorValue >> 8) & 0xff
        const b = (colorValue >> 16) & 0xff
        this.colorPrefix = 'rgba(' + r + ', ' + g + ', ' + b + ', '
        this.yRange = this.yres + velocity[1] * WinterSnow.MaxLife
    }

    private reinitFlake(s: FlakeState) {
        s.x = Math.floor(Math.random() * this.xres)
        s.y = this.yres - Math.floor(Math.random() * this.yRange)
        s.vx = Math.floor(Math.random() * 3) - 1
        s.life = Math.floor(Math.random() * WinterSnow.MaxLife)
    }

    update() {
        for (let i = 0; i < this.count; ++i) {
            const p = this.flakes[i]
            p.x += p.vx + this.velocity[0]
            p.y += 1 + this.velocity[1]
            p.life -= 1
            if (p.x < 0
                    || p.x >= this.xres
                    || p.y >= this.yres
                    || p.life <= 0) {
                this.reinitFlake(p)
            }
        }
    }

    draw(canvasEl: HTMLCanvasElement) {
        const ctx = canvasEl.getContext('2d')
        if (ctx === null) {
            return
        }
        ctx.imageSmoothingEnabled = false
        for (let p of this.flakes) {
            const a = Math.sin(p.life / WinterSnow.MaxLife * Math.PI)
            ctx.fillStyle = this.colorPrefix + a + ')'
            ctx.fillRect(Math.floor(p.x), Math.floor(p.y), 1, 1)
        }
    }
}
