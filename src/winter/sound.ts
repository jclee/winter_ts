// TODO DO NOT COMMIT - actually use
import { Thing } from "./thing.js"

export class SoundBase {
    public position = 0
    public loop = false
    public volume = 1.0

    Play() {}
    Pause() {}
}

export class Sound extends SoundBase {
    constructor(_fileName: string) { super() }

    // TODO DO NOT COMMIT - make work
    Play() {}
    Pause() {}
}

export class NullSound extends SoundBase {
}

export class RepeatableSound extends SoundBase {
    private sounds: Sound[]

    constructor(private fileName: string) {
        super()
        this.sounds = [new Sound(fileName)]
        this.sounds[0].loop = false
    }

    Play() {
        for (let s of this.sounds) {
            if (s.position === 0) {
                s.Play()
                return
            }
        }

        const s = new Sound(this.fileName)
        s.loop = false
        s.Play()
        this.sounds.push(s)
    }
}

// effects:

export const slash1 = new RepeatableSound('sfx/swing1.wav')
export const slash2 = new RepeatableSound('sfx/swing2.wav')
export const slash3 = new RepeatableSound('sfx/swing3.wav')
export const playerHurt = new NullSound()

export const achievement = new RepeatableSound('sfx/LevelUp.wav')

export const menuClick = new RepeatableSound('sfx/MenuClick.wav')
export const menuBuzz = new RepeatableSound('sfx/MenuBuzz.wav')

export const hearthRend = new RepeatableSound('sfx/HearthRend.wav')
export const crushingGale = new RepeatableSound('sfx/CrushingGale.wav')
export const healingRain = new RepeatableSound('sfx/HealingRain.wav')

export const monsterHit = new RepeatableSound('sfx/MonsterHit.wav')

export const anklebiterStrike = new Sound('sfx/AnklebiterStrike.wav')
export const anklebiterHurt = new NullSound() // new Sound('sfx/AnklebiterHurt.wav')
export const anklebiterDie = new RepeatableSound('sfx/AnklebiterDie.wav')

export const yetiStrike = new NullSound()
export const yetiHurt = [
    new Sound('sfx/YetiHurt1.wav'),
    new Sound('sfx/YetiHurt2.wav'),
    new Sound('sfx/YetiHurt3.wav'),
]
export const yetiDie = new Sound('sfx/YetiDie.wav')

export const soulReaverStrike = new NullSound()
export const soulReaverHurt = [
    new Sound('sfx/SoulReaverHurt1.wav'),
    new Sound('sfx/SoulReaverHurt2.wav'),
    new Sound('sfx/SoulReaverHurt3.wav'),
]
export const soulReaverDie = new Sound('sfx/SoulReaverDie.wav')

export const razorManeStrike = new RepeatableSound('sfx/RazormaneStrike.wav')
export const razorManeHurt = new RepeatableSound('sfx/RazormaneHurt.wav')
export const razorManeDie = new RepeatableSound('sfx/RazormaneDie.wav')

// other effects?

export class Crossfader extends Thing {
    private oldMusic: Sound[] = []
    public music: Sound | null = null
    private inc = 0.01
    constructor() { super() }

    reset(newMusic: Sound | null) {
        if (newMusic === this.music) {
            return
        }

        if (newMusic !== null && this.oldMusic.includes(newMusic)) {
            this.oldMusic = this.oldMusic.filter(m => m !== newMusic)
        }

        if (this.music !== null) {
            if (!this.oldMusic.includes(this.music)) {
                this.oldMusic.push(this.music)
            }

            this.music = newMusic
            if (this.music !== null) {
                this.music.volume = 0.0
                this.music.Play()
            }
        } else {
            this.music = newMusic
            if (this.music !== null) {
                this.music.volume = 1.0
                this.music.Play()
            }
        }
    }

    kill() {
        if (this.music) {
            this.music.volume = 0.0
            this.music.Pause()
            this.music = null
            for (let m of this.oldMusic) {
                m.volume = 0
            }
            this.oldMusic = []
        }
    }

    update() {
        const newOldMusic: Sound[] = []
        for (let m of this.oldMusic) {
            m.volume -= this.inc
            if (m.volume <= 0) {
                m.Pause()
            } else {
                newOldMusic.push(m)
            }
        }
        this.oldMusic = newOldMusic
        if (this.music !== null) {
            this.music.volume = Math.min(1.0, this.music.volume + this.inc)
        }

        return (this.oldMusic.length === 0 && (this.music === null || this.music.volume >= 1.0))
    }
}
