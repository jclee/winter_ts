import { StatSet } from "./StatSet.js"

export class SaveData {
    constructor(
        public stats: StatSet,
        public flags: {[key: string]: string},
        public mapName: string,
        public playerX: number,
        public playerY: number,
        public playerLayer: number,
    ) {}
}

export function saveGame(index: number, saveData: SaveData) {
    const json = JSON.stringify(saveData)
    window.localStorage.setItem(`wintergame/save${index}`, json)
}

export function loadGame(index: number): SaveData | null {
    const s = window.localStorage.getItem(`wintergame/save${index}`)
    if (s === null) {
        return null
    }
    try {
        // TODO - stricter checking?
        const data = JSON.parse(s)
        const stats = new StatSet()
        stats.att = data.stats.att
        stats.exp = data.stats.exp
        stats.level = data.stats.level
        stats.mag = data.stats.mag
        stats.maxhp = data.stats.maxhp
        stats.maxmp = data.stats.maxmp
        stats.mres = data.stats.mres
        stats.next = data.stats.next
        stats.pres = data.stats.pres
        stats.hp = data.stats._hp
        stats.mp = data.stats._mp

        return new SaveData(
            stats,
            data.flags,
            data.mapName,
            data.playerX,
            data.playerY,
            data.playerLayer,
        )
    } catch (e) {}
    return null
}
