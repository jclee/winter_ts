import { PyEngine } from './../winter.js'

export class MapScript {
    constructor(
        public autoexec: (engineRef: PyEngine) => void = (_e: PyEngine) => {},
        public fns: {[key: string]: (engineRef: PyEngine) => IterableIterator<null>} = {},
    ) {}
}
