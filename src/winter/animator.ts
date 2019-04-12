export function makeAnim(strand: number[], delay: number): [number, number][] {
    // Quicky function to make a proper strand, given a
    // list of frames, and a delay between each.

    const fn: (f: number)=>[number, number] = f => [f, delay]
    return strand.map(fn)
}

export function makeAnimRange(start: number, end: number, delay: number): [number, number][] {
    const strand = []
    for (let i = start; i < end; ++i) {
        strand.push(i)
    }
    return makeAnim(strand, delay)
}

export class Animator {
    curFrame: number = 0
    index: number = 0
    isAnimating: boolean = false

    private _frameIndexTimePairs: [number, number][] = []
    private _count: number = 0
    private _loop: boolean = true

    start(frameIndexTimePairs: [number, number][], loop: boolean) {
        this._frameIndexTimePairs = frameIndexTimePairs
        this.curFrame = this._frameIndexTimePairs[0][0]
        this._count = this._frameIndexTimePairs[0][1]
        this.index = 0
        this.isAnimating = true
        this._loop = loop
    }

    stop() {
        this.isAnimating = false
    }

    update() {
        if (!this.isAnimating) {
            return
        }

        this._count -= 1
        while (this._count <= 0) {
            this.index += 1
            if (this.index >= this._frameIndexTimePairs.length) {
                if (this._loop) {
                    this.index = 0
                } else {
                    this.isAnimating = false
                    return
                }
            }

            this.curFrame = this._frameIndexTimePairs[this.index][0]
            this._count += this._frameIndexTimePairs[this.index][1]
        }
    }
}


