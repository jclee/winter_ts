import { PyEngine } from "./winter.js";

export class Field {
    // A field is just a big invisible thing that does something if the player
    // walks on to it.  Warp points can be fields, as can plot-based zone
    // thingies.

    constructor(
        private rect: [number, number, number, number],
        private layer: number,
        public scriptTask: (engine: PyEngine)=>IterableIterator<any>,
    ) {}

    test(layer: number, rx: number, ry: number, rw: number, rh: number) {
        const [x, y, w, h] = this.rect
        const result = (
            layer === this.layer
            && x - rw < rx
            && rx < x + w
            && y - rh < ry
            && ry < y + h
        )
        return result
    }
}
