export class StatSet {
    att: number = 0
    exp: number = 0
    level: number = 0
    mag: number = 0
    maxhp: number = 0
    maxmp: number = 0
    mres: number = 0
    next: number = 0
    pres: number = 0

    private _hp: number = 0
    private _mp: number = 0

    get hp(): number { return this._hp }
    set hp(v: number) {
        this._hp = Math.max(0, Math.min(this.maxhp, v))
    }

    get mp(): number { return this._mp }
    set mp(v: number) {
        this._mp = Math.max(0, Math.min(this.maxmp, v))
    }

    clone(): StatSet {
        const s = new StatSet()

        s._hp = this._hp
        s._mp = this._mp
        s.att = this.att
        s.exp = this.exp
        s.level = this.level
        s.mag = this.mag
        s.maxhp = this.maxhp
        s.maxmp = this.maxmp
        s.mres = this.mres
        s.next = this.next
        s.pres = this.pres

        return s
    }
}
