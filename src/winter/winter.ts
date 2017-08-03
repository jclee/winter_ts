
interface FlakeState {
    x: number;
    y: number;
    vx: number;
    life: number;
}

class WinterSnow {
    private static readonly Count = 1000;
    private static readonly MaxLife = 100;

    private flakes: FlakeState[];

    constructor(
        readonly xres: number,
        readonly yres: number,
        readonly velocity: [number, number]
    ) {
        this.flakes = [];
        for (let i = 0; i < WinterSnow.Count; ++i) {
            const flake = this.makeFlake();
            flake.life = Math.floor(Math.random() * WinterSnow.MaxLife);
            this.flakes.push(flake);
        }
    }

    private makeFlake() {
        return {
            x: Math.floor(Math.random() * this.xres),
            y: Math.floor(Math.random() * this.yres),
            vx: Math.floor(Math.random() * 3) - 1,
            life: 0
        };
    }

    update() {
        for (let i = 0; i < WinterSnow.Count; ++i) {
            const p = this.flakes[i];
            p.x += p.vx + this.velocity[0];
            p.y += 1 + this.velocity[1];
            p.life += 1;
            if (p.x < 0
                    || p.x >= this.xres
                    || p.y >= this.yres
                    || p.life >= WinterSnow.MaxLife) {
                this.flakes[i] = this.makeFlake();
            }
        }
    }

    draw(canvasEl : HTMLCanvasElement) {
        const ctx = canvasEl.getContext('2d');
        if (ctx === null) {
            return;
        }
        ctx.imageSmoothingEnabled = false;
        for (let p of this.flakes) {
            const a = Math.sin(p.life / WinterSnow.MaxLife * Math.PI);
            ctx.fillStyle = 'rgba(255, 255, 255, ' + a + ')';
            ctx.fillRect(Math.floor(p.x), Math.floor(p.y), 1, 1);
        }
    }
}
(window as any).WinterSnow = WinterSnow;

const removeChildren = (node : HTMLElement) => {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
};

const addPythonScript = (path : string) => {
    const s = document.createElement('script');
    s.type = 'text/python';
    s.src = path;
    document.body.appendChild(s);
};

const enum BrythonDebugLevel {
    None = 0,
    ShowErrors = 1,
    Translate = 2,
    TranslateAll = 10,
}

interface BrythonOptions {
    debug: BrythonDebugLevel;
}

declare var brython: (options: BrythonOptions) => void;

removeChildren(document.body);
addPythonScript('main.py');
brython({
    debug: BrythonDebugLevel.ShowErrors,
});
