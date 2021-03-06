
import { AnkleBiter, Carnivore, Devourer } from "./anklebiter.js"
import { sceneTask } from "./cabin.js"
import { Camera } from "./camera.js"
import { Caption } from "./caption.js"
import { Direction } from "./Direction.js"
import { Dynamite } from "./dynamite.js"
import { blurFadeTask, createBlurImages, fadeInTask, fadeOutTask, freeBlurImages } from "./effects.js"
import { creditsTask } from "./ending.js"
import { Entity } from "./entity.js"
import { Field } from "./field.js"
import { EXPBar, HPBar, MPBar } from "./hud.js"
import { introTask, menuTask } from "./intro.js"
import { IceWall, Gap, IceChunks, Boulder } from "./obstacle.js"
import { Player, PLAYER_SPRITE } from "./player.js"
import { MapScript } from "./maps/mapscript.js"
import { mapScripts } from "./maps/mapscripts.js"
import { DragonPup, HellHound, RazorMane } from "./razormane.js"
import { CowardRune, FireRune, GuardRune, PowerRune, StrengthRune, WaterRune, WindRune } from "./rune.js"
import { loadGame, SaveData, saveGame } from "./saveload.js"
import { loadMenuTask, saveMenuTask } from "./saveloadmenu.js"
import { SavePoint } from "./savepoint.js"
import { Crossfader, NullSound, Sound } from "./sound.js"
import { PauseScreen } from "./subscreen.js"
import { Thing } from "./thing.js"
import { Gorilla, SoulReaver, Yeti } from "./yeti.js"

// Can be useful to disable when trying to conserve power...
let drawFancySnow = true
let showIntroLogos = false

interface Size {
    width: number
    height: number
}

class Point {
    x: number = 0
    y: number = 0
}

interface MapData {
    information: MapInformation
    header: MapHeader
    layers: MapLayer[]
    zones: MapZoneScript[]
}

interface MapInformation {
    meta: {[key: string]: string}
}

interface MapHeader {
    dimensions: Size
    tileset: string
}

interface MapLayer {
    label: string
    dimensions: Size
    position: Point
    parallax: MapLayerParallax
    data: number[]
    obstructions: number[]
    entities: MapEntityData[]
    zones: MapZone[]
}

interface MapEntityData {
    x: number,
    y: number,
    label: string,
    sprite: string,
}

interface MapLayerParallax {
    mulx: number
    muly: number
    divx: number
    divy: number
}

interface MapZone {
    label: string
    x: number
    y: number
    width: number
    height: number
}

interface MapZoneScript {
    label: string
    script: string
}

export interface Image {
    _texture: WebGLTexture
    width: number
    height: number
    yScale: number
}

class Control {
    private pressed: number = 0
    private position: number = 0

    handleKeyDown() {
        this.pressed = 1
        this.position = 1
    }

    handleKeyUp() {
        this.position = 0
    }

    getPressed() {
        const p = this.pressed
        this.pressed = 0
        return p
    }

    getPosition() {
        return this.position
    }
}

class Input {
    private keys: {[key:string]: Control}

    constructor() {
        this.keys = {}
    }

    getKey(key: string): Control {
        if (this.keys[key] === undefined) {
            this.keys[key] = new Control()
        }
        return this.keys[key]
    }
}

class Canvas {
    constructor(
        public _image: Image,
        public _framebuffer: WebGLFramebuffer,
    ) {}
}

export class Sprite {
    // TODO: Probably a bunch of these members can be private, as the game does
    // not access them.

    specframe: number
    spritewidth: number
    spriteheight: number
    hotx: number
    hoty: number

    destLocation: Point
    destVector: Point
    speed: number
    isobs: boolean
    mapobs: boolean
    entobs: boolean
    _delayCount: number
    _speedCount: number
    hotwidth: number
    hotheight: number
    _direction: string
    isMoving: boolean
    // TODO: Only necessary to hide cyclical reference from Brython:
    _getEngine: ()=>Engine

    constructor(
        public x: number,
        public y: number,
        public layer: number,
        public spritename: string,
        public name: string,
        spriteData: SpriteData,
        engine: Engine,
    ) {
        this._getEngine = ()=>engine

        this.specframe = -1
        this.name = name

        this.speed = 100
        this.isobs = true
        this.mapobs = true
        this.entobs = true

        this.spritewidth = spriteData.width
        this.spriteheight = spriteData.height
        this.hotx = spriteData.hotspotX
        this.hoty = spriteData.hotspotY
        this.hotwidth = spriteData.hotspotWidth
        this.hotheight = spriteData.hotspotHeight

        this._direction = 'down'
        this.isMoving = false

        this._delayCount = 0
        this._speedCount = 0
        this.destLocation = new Point()
        this.destVector = new Point()
    }

    moveTo(x: number, y: number) {
        this.destLocation.x = x
        this.destLocation.y = y
        this.destVector.x = x - this.x
        this.destVector.y = y - this.y
        this._delayCount = 0

        // The code setting this flag seems to be missing in the ika source,
        // but seems to be necessary for the expected AI behavior seen in the
        // shipped game?
        this.isMoving = this.destVector.x != 0 || this.destVector.y != 0
    }

    stop() {
        this.destLocation.x = this.x
        this.destLocation.y = this.y
        this.destVector.x = 0
        this.destVector.y = 0
        this.isMoving = false
    }

    _update() {
        let newDir = ''

        // TODO: Don't know if animation scripts are being used yet.
        // TODO: Not handling player logic, since game doesn't seem to hook
        // up a player entity.
        // TODO: Not dealing with movescripts.

        // TODO: Can probably remove _delayCount: Wait not used.
        if (this._delayCount > 0) {
            this._delayCount -= 1
        } else if (this.destVector.x != 0 || this.destVector.y != 0) {
            const startX = this.destLocation.x - this.destVector.x
            const startY = this.destLocation.y - this.destVector.y
            const dx = this.x - this.destLocation.x
            const dy = this.y - this.destLocation.y
            if (dx == 0) {
                if (this.y > this.destLocation.y) {
                    newDir = 'up'
                } else if (this.y < this.destLocation.y) {
                    newDir = 'down'
                } else {
                    newDir = ''
                }
            } else if (dy == 0) {
                if (this.x > this.destLocation.x) {
                    newDir = 'left'
                } else if (this.x < this.destLocation.x) {
                    newDir = 'right'
                } else {
                    newDir = ''
                }
            } else {
                const m = this.destVector.y / this.destVector.x
                let targetY = Math.floor(Math.floor((this.x - startX) * m) + startY)
                let deltaY = Math.abs(this.y - targetY)
                if (deltaY == 0) {
                    var tempX
                    if (this.x > this.destLocation.x) {
                        newDir = 'left'
                        tempX = this.x - 1
                    } else {
                        newDir = 'right'
                        tempX = this.x + 1
                    }
                    targetY = Math.floor((tempX - startX) * m) + startY
                    deltaY = Math.abs(this.y - targetY)
                }
                if (deltaY == 1) {
                    if (this.y > this.destLocation.y) {
                        if (this.x > this.destLocation.x) {
                            newDir = 'upleft'
                        } else {
                            newDir = 'upright'
                        }
                    } else {
                        if (this.x > this.destLocation.x) {
                            newDir = 'downleft'
                        } else {
                            newDir = 'downright'
                        }
                    }
                } else if (deltaY > 1) {
                    if (this.y > this.destLocation.y) {
                        newDir = 'up'
                    } else {
                        newDir = 'down'
                    }
                }
            }
        }
        if (newDir == '') {
            this.stop()
        } else {
            this._move(newDir)
        }
    }

    private _moveDiagonally(d: string): string {
        let d1 = ''
        let d2 = ''
        if (d == 'upleft') {
            ;[d1, d2] = ['up', 'left']
        } else if (d == 'upright') {
            ;[d1, d2] = ['up', 'right']
        } else if (d == 'downleft') {
            ;[d1, d2] = ['down', 'left']
        } else if (d == 'downright') {
            ;[d1, d2] = ['down', 'right']
        } else {
            return d
        }

        const newX = this.x + (d2 == 'left' ? -1 : 1)
        const newY = this.y + (d1 == 'up' ? -1 : 1)

        if (this._isObstructedAt(this.x, newY)) {
            d1 = ''
        }
        if (this._isObstructedAt(newX, this.y)) {
            d2 = ''
        }

        if (d1 == '') {
            return d2
        }
        if (d2 == '') {
            return d1
        }

        if (d1 == 'up') {
            return (d2 == 'left' ? 'upleft' : 'upright')
        } else {
            return (d2 == 'left' ? 'downleft' : 'downright')
        }
    }

    private _move(newDir: string) {
        const moveDir = this._moveDiagonally(newDir)
        this._direction = newDir

        // TODO Not dealing with animscript
        this.isMoving = true

        let newX = this.x
        let newY = this.y
        if (moveDir == 'up') {
            newY -= 1
        } else if (moveDir == 'down') {
            newY += 1
        } else if (moveDir == 'left') {
            newX -= 1
        } else if (moveDir == 'right') {
            newX += 1
        } else if (moveDir == 'upleft') {
            newY -= 1
            newX -= 1
        } else if (moveDir == 'upright') {
            newY -= 1
            newX += 1
        } else if (moveDir == 'downleft') {
            newY += 1
            newX -= 1
        } else if (moveDir == 'downright') {
            newY += 1
            newX += 1
        }
        if (this._isObstructedAt(newX, newY)) {
            this.stop()
            return
        }
        this.x = newX
        this.y = newY
    }

    private _isObstructedAt(x: number, y: number): boolean {
        const engine = this._getEngine()
        return (
            (this.mapobs && engine.detectMapCollision(x, y, this.hotwidth, this.hotheight, this.layer))
            || (this.entobs && engine.detectSpriteCollision(this.name, x, y, this.hotwidth, this.hotheight, this.layer))
        )
    }

    touches(otherSprite: Sprite): boolean {
        const x1 = this.x
        const y1 = this.y
        const w = this.hotwidth
        const h = this.hotheight

        if (x1     > otherSprite.x + otherSprite.hotwidth ||
            y1     > otherSprite.y + otherSprite.hotheight ||
            x1 + w < otherSprite.x ||
            y1 + h < otherSprite.y)
        {
            return false
        } else {
            return true
        }
    }
}

interface FontData {
    subsets: number[][]
    widths: number[]
    heights: number[]
}

const _fontData : FontData = {
    subsets: [
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
            26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
            42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
            58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
            74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
            90, 91, 92, 93, 94, 95, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],
        [
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
            109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
            121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
            133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144,
            145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156,
            157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
            169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
            181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96
        ]
    ],
    widths: [
        7, 4, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 4, 7, 4, 7, 7, 6, 7, 7, 7, 7,
        7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7,
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7,
        7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 4, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
        7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 4, 7,
        4, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7,
        7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
        7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 4, 9, 7, 7,
        7, 7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7
    ],
    heights: [
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10
    ],
}

export class Font {
    height: number

    constructor(
        private _engine: Engine,
    ) {
        this.height = 10
    }

    // TODO: Other members?

    centerPrint(x: number, y: number, text: string) {
        this.print(x - this.stringWidth(text) / 2 , y, text)
    }

    stringWidth(s: string): number {
        let w = 0
        for (let glyph of this._genGlyphs(s)) {
            w += glyph.width
        }
        return w
    }

    printWithOpacity(x: number, y: number, text: string, opacity: number) {
        this._engine.targetPageFramebuffer()
        const image = this._engine.getImage('system_font.png')
        let cursorX = Math.floor(x)
        let cursorY = Math.floor(y)
        for (let glyph of this._genGlyphs(text)) {
            this._engine.drawImage(
                image,
                glyph.tileX,
                glyph.tileY,
                glyph.width,
                glyph.height,
                cursorX,
                cursorY,
                glyph.width,
                glyph.height,
                opacity)
            cursorX += glyph.width
        }
    }

    print(x: number, y: number, text: string) {
        this.printWithOpacity(x, y, text, 1.0)
    }

    *_genGlyphs(text:string) {
        const subsets = _fontData.subsets
        const widths = _fontData.widths
        const heights = _fontData.heights
        let index = 0
        let subsetIndex = 0
        while (index < text.length) {
            const ch = text.charAt(index)
            index += 1
            if (ch === '\n' || ch === '\t') {
                throw new Error("String codes not implemented")
            }
            if (ch == '~' && index < text.length) {
                const subsetCh = text.charAt(index)
                if (subsetCh >= '0' && subsetCh <= '9') {
                    index += 1
                    subsetIndex = subsetCh.charCodeAt(0) - '0'.charCodeAt(0)
                    continue
                }
            }
            const glyphIndex = subsets[subsetIndex][ch.charCodeAt(0)]
            yield {
                width: widths[glyphIndex],
                height: heights[glyphIndex],
                tileX: (glyphIndex % 16) * 9,
                tileY: Math.floor(glyphIndex / 16) * 10,
            }
        }
    }
}

class MapClass {
    private _xwin: number = 0
    private _ywin: number = 0
    private _localLayerDatas: number[][] = []
    // TODO: Make private?
    _localLayerObstructions: number[][] = []
    _currentMapName: string = ''
    private _spriteID: number
    // TODO: make private and provide different accessor?
    sprites: {[key: string]: Sprite}
    mapSpriteNames_: string[]
    layercount: number = 0

    constructor(
        private _engine: Engine,
        private _video: Video
    ) {
        this._spriteID = 0
        this.sprites = {}
        this.mapSpriteNames_ = []
    }

    get xwin(): number {
        return this._xwin
    }
    get ywin(): number {
        return this._ywin
    }
    set xwin(x: number) {
        this._setCamera(x, this._ywin)
    }
    set ywin(y: number) {
        this._setCamera(this._xwin, y)
    }

    private _setCamera(x: number, y: number) {
        const mapData = this._engine.getMapData(this._currentMapName)
        const dimensions = mapData.header.dimensions
        const width = dimensions.width
        const height = dimensions.height
        if (width > 0) {
            this._xwin = Math.max(0, Math.min(width - this._video.xres - 1, x))
        } else {
            this._xwin = x
        }
        if (height > 0) {
            this._ywin = Math.max(0, Math.min(height - this._video.yres - 1, y))
        } else {
            this._ywin = y
        }
    }

    render() {
        const mapData = this._engine.getMapData(this._currentMapName)

        // This game only uses the single tile map with this fixed size:
        const tileW = 16
        const tileH = 16
        const tilesPerRow = 16

        const layerCount = mapData.layers.length
        const layerSprites: [number, Sprite][][] = []
        for (let i = 0; i < layerCount; ++i) {
            layerSprites.push([])
        }
        // TODO: Better way to do this in typescript?  For..of something?
        for (let key in this.sprites) {
            const sprite = this.sprites[key]
            layerSprites[sprite.layer].push([sprite.y, sprite])
        }
        for (let layerSprite of layerSprites) {
            layerSprite.sort()
        }

        this._engine.targetPageFramebuffer()

        // This game only uses a single tile map:
        const image = this._engine.getImage('snowy.png')

        // SetCameraTarget (and SetPlayer, which calls it) are not used by the
        // game.

        // SetRenderList is not used by the game.
        for (let i = 0; i < layerCount; ++i) {
            const layer = mapData.layers[i]
            // This game doesn't use layer position
            const xw = Math.floor(this._xwin * layer.parallax.mulx / layer.parallax.divx)
            const yw = Math.floor(this._ywin * layer.parallax.muly / layer.parallax.divy)
            let firstX = Math.floor(xw / tileW)
            let firstY = Math.floor(yw / tileH)
            let adjustX = xw % tileW
            let adjustY = yw % tileH
            // This game doesn't use wrapped layers.

            const w = layer.dimensions.width
            const h = layer.dimensions.height
            let lenX = Math.floor(this._video.xres / tileW) + 1
            let lenY = Math.floor(this._video.yres / tileH) + 2

            if (firstX < 0) {
                lenX -= -firstX
                adjustX += firstX * tileW
                firstX = 0
            }
            if (firstY < 0) {
                lenY -= -firstY
                adjustY += firstY * tileH
                firstY = 0
            }
            if (firstX + lenX > w) {
                lenX = w - firstX
            }
            if (firstY + lenY > h) {
                lenY = h - firstY
            }

            const localLayerData = this._localLayerDatas[i]
            for (let y = 0; y < lenY; ++y) {
                for (let x = 0; x < lenX; ++x) {
                    const index = (firstY + y) * w + (firstX + x)
                    // This game doesn't use tile animations
                    const tileIndex = localLayerData[index]
                    // canvas drawing optimization: tile 0 is fully transparent.
                    if (tileIndex === 0) {
                        continue;
                    }
                    const tileX = (tileIndex % tilesPerRow) * tileW
                    const tileY = Math.floor(tileIndex / tilesPerRow) * tileH
                    this._engine.drawImage(
                        image,
                        tileX,
                        tileY,
                        tileW,
                        tileH,
                        x * tileW - adjustX,
                        y * tileH - adjustY,
                        tileW,
                        tileH,
                        1.0
                    )
                }
            }

            for (let kvPair of layerSprites[i]) {
                // This game doesn't seem to use custom renderscripts
                const sprite: Sprite = kvPair[1]

                const spritePath = 'sprite/' + sprite.spritename.replace('.ika-sprite', '.png')
                const spriteImage = this._engine.getImage(spritePath)

                const frameIndex = Math.max(0, sprite.specframe)
                const frameX = (frameIndex % 8) * sprite.spritewidth
                const frameY = Math.floor(frameIndex / 8) * sprite.spriteheight

                // This game doesn't use sprite visibility toggling.
                this._engine.drawImage(
                    spriteImage,
                    frameX,
                    frameY,
                    sprite.spritewidth,
                    sprite.spriteheight,
                    sprite.x - sprite.hotx - xw,
                    sprite.y - sprite.hoty - yw,
                    sprite.spritewidth,
                    sprite.spriteheight,
                    1.0
                )
            }
        }
        // This game doesn't use hookretrace.
    }

    setTile(x: number, y: number, layerIndex: number, tileIndex: number) {
        const mapData = this._engine.getMapData(this._currentMapName)
        const layer = mapData.layers[layerIndex]
        const localLayerData = this._localLayerDatas[layerIndex]
        const index = y * layer.dimensions.width + x
        localLayerData[index] = tileIndex
    }

    setObs(x: number, y: number, layerIndex: number, obs: number) {
        const mapData = this._engine.getMapData(this._currentMapName)
        const layer = mapData.layers[layerIndex]
        const localLayerObstructions = this._localLayerObstructions[layerIndex]
        const index = y * layer.dimensions.width + x
        localLayerObstructions[index] = obs
    }

    load(path: string) {
        // Clear old map-associated sprites, keeping dynamically added sprites.
        for (let name of this.mapSpriteNames_) {
            delete this.sprites[name]
        }
        this.mapSpriteNames_ = []

        this._currentMapName = path.replace('.ika-map', '')
        this._xwin = 0
        this._ywin = 0

        const mapData = this._engine.getMapData(this._currentMapName)
        this.layercount = mapData.layers.length

        // We need to clone layer data, since scripts can mutate the tile
        // content.
        this._localLayerDatas = []
        this._localLayerObstructions = []
        for (let i = 0; i < mapData.layers.length; ++i) {
            const layer = mapData.layers[i]
            this._localLayerDatas.push(layer.data.slice(0))
            this._localLayerObstructions.push(layer.obstructions.slice(0))
        }

        for (let i = 0; i < mapData.layers.length; ++i) {
            const layer = mapData.layers[i]
            for (let entity of layer.entities) {
                const spriteData = this._engine.sprites[entity.sprite]
                const sprite = new Sprite(
                    entity.x,
                    entity.y,
                    i,
                    entity.sprite,
                    entity.label,
                    spriteData,
                    this._engine,
                )
                this.sprites[sprite.name] = sprite
                this.mapSpriteNames_.push(sprite.name)
            }
        }
    }

    getMetaData() {
        const mapData = this._engine.getMapData(this._currentMapName)
        return mapData.information.meta
    }

    getZones(layerIndex: number): [number, number, number, number, string][] {
        let zoneTuples: [number, number, number, number, string][] = []
        const mapData = this._engine.getMapData(this._currentMapName)

        for (let zone of mapData.layers[layerIndex].zones) {
            let scriptName = null
            for (let zoneMetadata of mapData.zones) {
                if (zoneMetadata.label === zone.label) {
                    scriptName = zoneMetadata.script
                    break
                }
            }
            if (scriptName === null) {
                throw new Error("Unrecognized script name")
            }
            zoneTuples.push([
                zone.x,
                zone.y,
                zone.width,
                zone.height,
                scriptName
            ])
        }
        return zoneTuples
    }

    findLayerByName(name: string): number | null {
        const mapData = this._engine.getMapData(this._currentMapName)
        for (let i = 0; i < mapData.layers.length; ++i) {
            const layer = mapData.layers[i]
            if (layer.label === name) {
                return i
            }
        }
        return null
    }

    addSprite(x: number, y: number, layer: number, spritename: string) {
        this._spriteID += 1
        const name = "sprite_" + this._spriteID
        const spriteData = this._engine.sprites[spritename]
        const sprite = new Sprite(x, y, layer, spritename, name, spriteData, this._engine)
        this.sprites[sprite.name] = sprite
        return sprite
    }
    removeSprite(sprite: Sprite) {
        delete this.sprites[sprite.name]
    }
    spritesAt(x: number, y: number, width: number, height: number, layer: number) {
        const x2 = x + width
        const y2 = y + height

        const found = []
        for (let key in this.sprites) {
            const sprite = this.sprites[key]
            if (sprite.layer != layer) {
                continue
            }
            if (x > sprite.x + sprite.hotwidth) {
                continue
            }
            if (y > sprite.y + sprite.hotheight) {
                continue
            }
            if (x2 < sprite.x) {
                continue
            }
            if (y2 < sprite.y) {
                continue
            }
            found.push(sprite)
        }
        return found
    }
    processSprites() {
        const _TIME_RATE = 100
        for (let key in this.sprites) {
            const sprite = this.sprites[key]
            sprite._speedCount += sprite.speed
            while (sprite._speedCount >= _TIME_RATE) {
                sprite._update()
                sprite._speedCount -= _TIME_RATE
            }
        }
    }
}

interface SpriteData {
    width: number
    height: number
    count: number
    hotspotX: number
    hotspotY: number
    hotspotWidth: number
    hotspotHeight: number
}

interface ShaderSpec {
    vertex: string
    fragment: string
}

interface GfxProgram {
    program: WebGLProgram
    attributes: {[key: string]: number}
    uniforms: {[key: string]: WebGLUniformLocation}
    attributeLocations: number[]
}

// Not a general solution, but good enough for our purposes:
const _attributeRegex = /\battribute\s+\S+\s+([^;]+);/g
const _uniformRegex = /\buniform\s+\S+\s+([^;]+);/g

const _makeProgram = (gl: WebGLRenderingContext, shaderSpec: ShaderSpec) => {
    const makeShader = (gl: WebGLRenderingContext, type: number, source: string) => {
        const shader = gl.createShader(type)
        if (shader === null) {
            throw new Error("Couldn't create shader")
        }
        gl.shaderSource(shader, source)
        gl.compileShader(shader)
        const success = gl.getShaderParameter(shader, gl.COMPILE_STATUS)
        if (!success) {
            console.log(gl.getShaderInfoLog(shader))
            gl.deleteShader(shader)
            throw new Error("Couldn't compile shader")
        }
        return shader
    }

    const vertexShader = makeShader(gl, gl.VERTEX_SHADER, shaderSpec.vertex)
    const fragmentShader = makeShader(gl, gl.FRAGMENT_SHADER, shaderSpec.fragment)
    const combined = (shaderSpec.vertex + '\n' + shaderSpec.fragment);
    const getMatching = (regexp: RegExp) => {
        const regexpCopy = new RegExp(regexp)
        let captures = []
        let match
        while (match = regexpCopy.exec(combined)) {
            captures.push(match[1])
        }
        return [...new Set(captures)]
    }

    const attributeNames = getMatching(_attributeRegex)
    const uniformNames = getMatching(_uniformRegex)

    const program = gl.createProgram()
    if (program === null) {
        throw new Error("Couldn't create shader program")
    }
    try {
        gl.attachShader(program, vertexShader)
        gl.attachShader(program, fragmentShader)
        gl.linkProgram(program)
        const success = gl.getProgramParameter(program, gl.LINK_STATUS)
        if (!success) {
            console.log(gl.getProgramInfoLog(program))
            throw new Error("Couldn't link program")
        }
        const attributes: {[key: string]: number} = {}
        const attributeLocations: number[] = []
        attributeNames.forEach((name) => {
            const loc = gl.getAttribLocation(program, name)
            attributes[name] = loc
            attributeLocations.push(loc)
        })
        const uniforms: {[key: string]: WebGLUniformLocation} = {}
        uniformNames.forEach((name) => {
            const loc = gl.getUniformLocation(program, name)
            if (loc === null) {
                throw new Error(`Couldn't get shader uniform location: ${name}`)
            } else {
                uniforms[name] = loc
            }
        })

        attributeLocations.sort()

        const gfxProgram: GfxProgram = {
            program: program,
            attributes: attributes,
            uniforms: uniforms,
            attributeLocations: attributeLocations,
        }
        return gfxProgram
    } catch (e) {
        gl.deleteProgram(program)
        throw e
    }
}

const _makeTexture = (gl: WebGLRenderingContext) => {
    const texture = gl.createTexture()
    if (texture === null) {
        throw new Error("Couldn't create texture")
    }
    gl.bindTexture(gl.TEXTURE_2D, texture)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE)
    // Filters could be nearest, except Chrome doesn't like min filter
    // nearest with NPOT textures.
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
    return texture
}

const _makeEmptyTexture = (gl: WebGLRenderingContext, width: number, height: number) => {
    const texture = _makeTexture(gl)
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, width, height, 0, gl.RGB, gl.UNSIGNED_BYTE, null)
    return texture
}

const _makeImageTexture = (gl: WebGLRenderingContext, imageEl: HTMLImageElement) => {
    const texture = _makeTexture(gl)
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, imageEl)
    return texture
}

const _makeFramebuffer = (gl: WebGLRenderingContext, texture: WebGLTexture) => {
    const buffer = gl.createFramebuffer()
    if (buffer === null) {
        throw new Error("Couldn't create framebuffer")
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, buffer)
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0)
    return buffer
}

const _makeBuffer = (gl: WebGLRenderingContext, vals: number[]) => {
    const buffer = gl.createBuffer()
    if (buffer === null) {
        throw new Error("Couldn't create buffer")
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vals), gl.STATIC_DRAW)
    return buffer
}

const _textureShaderSpec = {
    vertex: (`
        precision mediump float;

        attribute vec4 a_position;
        attribute vec2 a_texCoord;
        // TODO: We use very few of these matrix entries...
        uniform mat4 u_matrix;
        uniform mat3 u_texMatrix;
        varying vec2 v_texCoord;

        void main() {
          gl_Position = u_matrix * a_position;
          v_texCoord = (u_texMatrix * vec3(a_texCoord, 1)).xy;
        }
    `),
    fragment: (`
        precision mediump float;

        uniform sampler2D u_image;
        uniform float u_opacity;
        varying vec2 v_texCoord;

        void main() {
          vec4 color = texture2D(u_image, v_texCoord);
          gl_FragColor = vec4(color.rgb, color.a * u_opacity);
        }
    `),
}

const _flatShaderSpec = {
    vertex: (`
        precision mediump float;

        attribute vec4 a_position;
        // TODO: We use very few of these matrix entries...
        uniform mat4 u_matrix;

        void main() {
          gl_Position = u_matrix * a_position;
        }
    `),
    fragment: (`
        precision mediump float;

        uniform vec4 u_color;

        void main() {
          gl_FragColor = u_color;
        }
    `),
}

const _snowShaderSpec = {
    vertex: (`
        precision mediump float;

        attribute vec4 a_position;
        attribute vec2 a_texCoord;
        varying vec2 v_texCoord;

        void main() {
          gl_Position = vec4(
              2.0 * a_position.xy - vec2(1.0, 1.0),
              0.0,
              1.0
          );
          v_texCoord = vec3(a_texCoord, 1).xy;
        }
    `),
    fragment: (`
        #define M_PI 3.14159265358979323846

        precision mediump float;

        uniform float u_time;
        uniform float u_count;
        uniform vec2 u_size;
        uniform vec2 u_velocity;
        uniform vec3 u_color;
        varying vec2 v_texCoord;

        // From: https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83
        float rand(vec2 n) {
            return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
        }
        float noise(vec2 n) {
            const vec2 d = vec2(0.0, 1.0);
            vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
            return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
        }

        float sortaSnow(vec2 v, float t) {
          float x = noise(v * 160.0);

          return clamp(mix(-100000.0 / u_count, 1.0, abs(fract(x * 2.0 + t * u_count * 0.0000001) * 2.0 - 1.0)), 0.0, 1.0);
        }

        void main() {
          float t = floor(u_time / 16.667) + 1000.0;
          vec2 s = vec2(1.0 / u_size.x, 1.0 / u_size.y);
          vec2 d1 = (u_velocity + vec2(0.0, 1.0)) * t;
          vec2 d2 = (u_velocity + vec2(1.0, 1.0)) * t;
          vec2 d3 = (u_velocity + vec2(-1.0, 1.0)) * t;
          float snow1 = sortaSnow(v_texCoord + floor(d1) * s, t);
          float snow2 = sortaSnow(v_texCoord + floor(d2) * s, t + 10000.0);
          float snow3 = sortaSnow(v_texCoord + floor(d3) * s, t - 10000.0);
          float a = clamp(snow1 + snow2 + snow3, 0.0, 1.0);
          gl_FragColor = a * vec4(u_color, 1.0);
        }
    `),
}

let _canvases: Canvas[] = []

class Video {
    // Resolution used in this game...
    readonly xres = 320
    readonly yres = 240
    // TODO: Only necessary to hide cyclical reference from Brython:
    private _getEngine: ()=>Engine

    constructor(
        engine: Engine,
    ) {
        this._getEngine = ()=>engine
    }

    blit(image: Image, x: number, y: number) {
        this.tintScaleBlit(image, x, y, image.width, image.height, 1.0)
    }

    clearScreen() {
        const engine = this._getEngine()
        const gl = engine.gl
        engine.targetPageFramebuffer()
        gl.clearColor(0, 0, 0, 1.0)
        gl.clear(gl.COLOR_BUFFER_BIT)
    }

    drawRect(x1: number, y1: number, x2: number, y2: number, r: number, g: number, b: number, opacity: number) {
        const engine = this._getEngine()
        engine.targetPageFramebuffer()
        engine.drawRect(x1, y1, x2 - x1 + 1, y2 - y1 + 1, r, g, b, opacity)
    }

    grabImage(x1: number, y1: number, x2: number, y2: number) {
        const engine = this._getEngine()
        const gl = engine.gl

        const width = x2 - x1
        const height = y2 - y1
        const image = {
            _texture: _makeEmptyTexture(gl, width, height),
            width: width,
            height: height,
            yScale: -1.0,
        }
        const framebuffer = _makeFramebuffer(gl, image._texture)

        const canvas = new Canvas(image, framebuffer)
        engine.targetCanvas(canvas)

        gl.clearColor(1.0, 0, 0, 1.0)
        gl.clear(gl.COLOR_BUFFER_BIT)

        engine.drawImage(engine.pageImage, 0, 0, engine.pageImage.width, engine.pageImage.height, -x1, -y1, engine.pageImage.width, engine.pageImage.height, 1.0)

        _canvases.push(canvas)
        return canvas._image
    }

    freeImage(image: Image) {
        const engine = this._getEngine()
        const gl = engine.gl

        let canvas: Canvas | null = null
        _canvases = _canvases.filter((x: Canvas) => {
            if (x._image === image) {
                canvas = x
            }
            return x._image !== image
        })
        if (canvas === null) {
            throw new Error("Tried to free inactive canvas")
        } else {
            const canvas2: Canvas = canvas
            // Good idea?
            gl.bindFramebuffer(gl.FRAMEBUFFER, null)
            gl.bindTexture(gl.TEXTURE_2D, null)
            gl.deleteFramebuffer(canvas2._framebuffer)
            gl.deleteTexture(canvas2._image._texture)
        }
    }

    scaleBlit(image: Image, x: number, y: number, width: number, height: number) {
        this.tintScaleBlit(image, x, y, width, height, 1.0)
    }

    showPage() {
        const engine = this._getEngine()
        engine.targetCanvasFramebuffer()
        engine.drawImage(engine.pageImage, 0, 0, engine.pageImage.width, engine.pageImage.height, 0, 0, engine.pageImage.width, engine.pageImage.height, 1.0)

        // Makes compositing more reliable.  Some maps don't draw the whole screen.
        this.clearScreen()
    }

    tintBlit(image: Image, x: number, y: number, alpha: number) {
        this.tintScaleBlit(image, x, y, image.width, image.height, alpha)
    }

    tintScaleBlit(image: Image, x: number, y: number, width: number, height: number, alpha: number) {
        const engine = this._getEngine()
        engine.targetPageFramebuffer()
        engine.drawImage(image, 0, 0, image.width, image.height, x, y, width, height, alpha)
    }

    // TODO other members...
}

interface Controls {
    up: ()=>boolean
    down: ()=>boolean
    left: ()=>boolean
    right: ()=>boolean
    attack: ()=>boolean
    enter: ()=>boolean
    cancel: ()=>boolean
    rend: ()=>boolean
    gale: ()=>boolean
    heal: ()=>boolean
    shiver: ()=>boolean
}

export class Snow {
    private engine: Engine
    private time: number
    private vx: number
    private vy: number
    private r: number
    private g: number
    private b: number
    constructor(
        engineRef: PyEngine,
        private count=100,
        velocity=[0, 0.5],
        color=[255, 255, 255],
    ) {
        this.engine = engineRef.getEngine()
        this.time = 0.0
        this.vx = velocity[0]
        this.vy = velocity[1]
        this.r = color[0] / 255.0
        this.g = color[1] / 255.0
        this.b = color[2] / 255.0
    }

    update() {
        this.time += 10.0
        return false
    }

    draw() {
        if (drawFancySnow) {
            this.engine.drawSnow(this.time, this.count, this.vx, this.vy, this.r, this.g, this.b)
        }
    }
}

export function *delayTask(time: number) {
    const targetEnd = Date.now() + (time * 10)
    // Busy waiting, sort of... :(
    while (targetEnd > Date.now()) {
        yield null
    }
}

export function random(low: number, high: number) {
    return Math.floor(Math.random() * (high - low)) + low
}

export function hypot(x: number, y: number) {
    return Math.sqrt(x * x + y * y)
}

export class Engine {
    maps: {[key: string]: MapData}
    images: {[key: string]: Image}
    sprites: {[key: string]: SpriteData}
    sounds: {[key: string]: Sound}
    width = 320
    height = 240
    startMsec: number
    gl: WebGLRenderingContext
    private enabledAttributeLocations: number[]
    pageImage: Image
    private pageBuffer: WebGLFramebuffer
    private textureProgram: GfxProgram
    private flatProgram: GfxProgram
    private snowProgram: GfxProgram
    private viewWidth: number
    private viewHeight: number
    quadPositionBuffer: WebGLBuffer
    quadTexCoordBuffer: WebGLBuffer
    map: MapClass
    private input: Input
    controls: Controls
    video: Video

    constructor() {
        this.images = {}
        this.maps = {}
        this.sprites = {}
        this.sounds = {}
        this.input = new Input()
        this.video = new Video(this)
        this.map = new MapClass(this, this.video)
        this.enabledAttributeLocations = []

        const posControl = (s: string) => {
            const key = this.input.getKey(s)
            return () => key.getPosition() > 0
        }
        const pressControl = (s: string) => {
            const key = this.input.getKey(s)
            return () => key.getPressed() !== 0
        }
        this.controls = {
            up: posControl('UP'),
            down: posControl('DOWN'),
            left: posControl('LEFT'),
            right: posControl('RIGHT'),
            attack: pressControl('SPACE'),
            enter: pressControl('SPACE'),
            cancel: pressControl('ESCAPE'),
            rend: pressControl('Z'),
            gale: pressControl('X'),
            heal: pressControl('C'),
            shiver: pressControl('V'),
        }

        this.startMsec = Date.now()

        const displayCanvasEl = window.document.createElement('canvas')
        displayCanvasEl.width = this.width
        displayCanvasEl.height = this.height

        const style = displayCanvasEl.style
        style.border = "1px solid"
        // Typescript doesn't know about imageRendering yet.
        ;(style as any).imageRendering = "optimizeSpeed"
        ;(style as any).imageRendering = "-moz-crisp-edges"
        ;(style as any).imageRendering = "pixelated"
        style.width = "" + this.width * 2
        style.height = "" + this.height * 2
        style.display = "block"
        style.marginLeft = "auto"
        style.marginRight = "auto"
        window.document.body.appendChild(displayCanvasEl)
        window.document.body.style.backgroundColor = "#dddddd"

        const gl = displayCanvasEl.getContext('webgl', {alpha: false})
        if (gl === null) {
            throw new Error("Couldn't get WebGL context")
        }
        this.gl = gl

        this.pageImage = {
            _texture: _makeEmptyTexture(gl, this.width, this.height),
            width: this.width,
            height: this.height,
            yScale: -1.0,
        }
        this.pageBuffer = _makeFramebuffer(gl, this.pageImage._texture)

        this.textureProgram = _makeProgram(gl, _textureShaderSpec)
        this.flatProgram = _makeProgram(gl, _flatShaderSpec)
        this.snowProgram = _makeProgram(gl, _snowShaderSpec)

        this.quadPositionBuffer = _makeBuffer(gl, [
            0, 0,
            0, 1,
            1, 0,
            1, 0,
            0, 1,
            1, 1,
        ])
        this.quadTexCoordBuffer = _makeBuffer(gl, [
            0, 0,
            0, 1,
            1, 0,
            1, 0,
            0, 1,
            1, 1,
        ])
        this.viewWidth = this.width
        this.viewHeight = this.height
    }

    getTime() {
        const deltaMsec = Date.now() - this.startMsec
        return Math.floor(deltaMsec / 10)
    }

    targetCanvasFramebuffer() {
        const gl = this.gl
        gl.bindFramebuffer(gl.FRAMEBUFFER, null)
        gl.viewport(0, 0, gl.canvas.width, gl.canvas.height)
        this.viewWidth = gl.canvas.width
        this.viewHeight = gl.canvas.height
    }

    targetPageFramebuffer() {
        const gl = this.gl
        gl.bindFramebuffer(gl.FRAMEBUFFER, this.pageBuffer)
        gl.viewport(0, 0, gl.canvas.width, gl.canvas.height)
        this.viewWidth = gl.canvas.width
        this.viewHeight = gl.canvas.height
    }

    targetCanvas(canvas: Canvas) {
        const gl = this.gl
        gl.bindFramebuffer(gl.FRAMEBUFFER, canvas._framebuffer)
        gl.viewport(0, 0, canvas._image.width, canvas._image.height)
        this.viewWidth = canvas._image.width
        this.viewHeight = canvas._image.height
    }

    private _enableAttributes(program: GfxProgram) {
        if (program.attributeLocations === this.enabledAttributeLocations) {
            return
        }
        this.enabledAttributeLocations.forEach(x => {
            if (undefined === program.attributeLocations.find(y => y === x)) {
                this.gl.disableVertexAttribArray(x)
            }
        })
        program.attributeLocations.forEach(x => {
            if (undefined === this.enabledAttributeLocations.find(y => y === x)) {
                this.gl.enableVertexAttribArray(x)
            }
        })
        this.enabledAttributeLocations = program.attributeLocations
    }

    drawRect(
        x: number,
        y: number,
        w: number,
        h: number,
        r: number,
        g: number,
        b: number,
        a: number
    ) {
        const gl = this.gl

        gl.enable(gl.BLEND)
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)

        gl.useProgram(this.flatProgram.program)
        this._enableAttributes(this.flatProgram)
        gl.bindBuffer(gl.ARRAY_BUFFER, this.quadPositionBuffer)
        gl.vertexAttribPointer(this.flatProgram.attributes.a_position, 2, gl.FLOAT, false, 0, 0)

        const viewW = this.viewWidth
        const viewH = this.viewHeight

        // Build xform from destination texture space to world space.
        const xs1 = w
        const xo1 = x
        const ys1 = h
        const yo1 = (viewH - (y + h))

        // Concat xform from world space to clip space.
        const xs2 = xs1 * 2.0 / viewW
        const xo2 = xo1 * 2.0 / viewW - 1.0
        const ys2 = ys1 * 2.0 / viewH
        const yo2 = yo1 * 2.0 / viewH - 1.0

        gl.uniformMatrix4fv(this.flatProgram.uniforms.u_matrix, false, [
            xs2, 0  , 0, 0,
            0  , ys2, 0, 0,
            0  , 0  , 1, 0,
            xo2, yo2, 0, 1,
        ])

        gl.uniform4f(this.flatProgram.uniforms.u_color, r, g, b, a)
        gl.drawArrays(gl.TRIANGLES, 0, 6)
    }

    drawImage(
        image: Image,
        srcX: number,
        srcY: number,
        srcW: number,
        srcH: number,
        destX: number,
        destY: number,
        destW: number,
        destH: number,
        opacity: number
    ) {
        const gl = this.gl

        gl.enable(gl.BLEND)
        // Dynamically generated textures are probably premultiplied, but
        // should have solid alpha so it shouldn't matter.
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)

        gl.useProgram(this.textureProgram.program)
        this._enableAttributes(this.textureProgram)
        gl.bindBuffer(gl.ARRAY_BUFFER, this.quadPositionBuffer)
        gl.vertexAttribPointer(this.textureProgram.attributes.a_position, 2, gl.FLOAT, false, 0, 0)
        gl.bindBuffer(gl.ARRAY_BUFFER, this.quadTexCoordBuffer)
        gl.vertexAttribPointer(this.textureProgram.attributes.a_texCoord, 2, gl.FLOAT, false, 0, 0)

        const viewW = this.viewWidth
        const viewH = this.viewHeight

        // Build xform from destination texture space to world space.
        const xs1 = destW
        const xo1 = destX
        const ys1 = destH
        const yo1 = (viewH - (destY + destH))

        // Concat xform from world space to clip space.
        const xs2 = xs1 * 2.0 / viewW
        const xo2 = xo1 * 2.0 / viewW - 1.0
        const ys2 = ys1 * 2.0 / viewH
        const yo2 = yo1 * 2.0 / viewH - 1.0

        gl.uniformMatrix4fv(this.textureProgram.uniforms.u_matrix, false, [
            xs2, 0  , 0, 0,
            0  , ys2, 0, 0,
            0  , 0  , 1, 0,
            xo2, yo2, 0, 1,
        ])

        // Build xform from unit square to source texture space
        const xs3 = srcW / image.width
        const xo3 = srcX / image.width
        const ys3 = -srcH / image.height
        const yo3 = (srcY + srcH) / image.height

        // Concat xform from source texture space to (maybe flipped) image space
        const xs4 = xs3
        const xo4 = xo3
        const ys4 = ys3 * image.yScale
        const yo4 = yo3 * image.yScale + 0.5 - image.yScale * 0.5

        gl.uniformMatrix3fv(this.textureProgram.uniforms.u_texMatrix, false, [
            xs4, 0  , 0,
            0  , ys4, 0,
            xo4, yo4, 1,
        ])

        gl.uniform1f(this.textureProgram.uniforms.u_opacity, opacity)
        gl.bindTexture(gl.TEXTURE_2D, image._texture)
        if (image._texture === undefined) {
            console.error("drawImage texture null")
        }
        gl.uniform1i(this.textureProgram.uniforms.u_image, 0)
        gl.drawArrays(gl.TRIANGLES, 0, 6)
    }

    drawSnow(
        time: number,
        count: number,
        vx: number,
        vy: number,
        r: number,
        g: number,
        b: number
    ) {
        this.targetPageFramebuffer()

        const gl = this.gl

        gl.enable(gl.BLEND)
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)

        gl.useProgram(this.snowProgram.program)
        this._enableAttributes(this.snowProgram)
        gl.bindBuffer(gl.ARRAY_BUFFER, this.quadPositionBuffer)
        gl.vertexAttribPointer(this.snowProgram.attributes.a_position, 2, gl.FLOAT, false, 0, 0)
        gl.bindBuffer(gl.ARRAY_BUFFER, this.quadTexCoordBuffer)
        gl.vertexAttribPointer(this.snowProgram.attributes.a_texCoord, 2, gl.FLOAT, false, 0, 0)

        gl.uniform1f(this.snowProgram.uniforms.u_time, time)
        gl.uniform1f(this.snowProgram.uniforms.u_count, count)
        gl.uniform2f(this.snowProgram.uniforms.u_size, this.viewWidth, this.viewHeight)
        gl.uniform2f(this.snowProgram.uniforms.u_velocity, vx, vy)
        gl.uniform3f(this.snowProgram.uniforms.u_color, r, g, b)
        // TODO - also, count, velocity?

        gl.drawArrays(gl.TRIANGLES, 0, 6)
    }

    run() {
        const imagePaths = [
            'winter/gfx/credits_vignette.png',
            'winter/gfx/gba.png',
            'winter/gfx/isabigfatbitch.png',
            'winter/gfx/mountains.png',
            'winter/gfx/title.png',
            'winter/gfx/ui/barhp0.png',
            'winter/gfx/ui/barhp1.png',
            'winter/gfx/ui/barhp2.png',
            'winter/gfx/ui/barhp3.png',
            'winter/gfx/ui/barmp0.png',
            'winter/gfx/ui/barmp1.png',
            'winter/gfx/ui/barmp2.png',
            'winter/gfx/ui/barmp3.png',
            'winter/gfx/ui/icon_att.png',
            'winter/gfx/ui/icon_mag.png',
            'winter/gfx/ui/icon_mres.png',
            'winter/gfx/ui/icon_pres.png',
            'winter/gfx/ui/pointer.png',
            'winter/gfx/ui/win_background.png',
            'winter/gfx/ui/win_bottom.png',
            'winter/gfx/ui/win_bottom_left.png',
            'winter/gfx/ui/win_bottom_right.png',
            'winter/gfx/ui/win_left.png',
            'winter/gfx/ui/win_right.png',
            'winter/gfx/ui/win_top.png',
            'winter/gfx/ui/win_top_left.png',
            'winter/gfx/ui/win_top_right.png',
            'winter/gfx/yourmother.png',
            'winter/snowy.png',
            'winter/sprite/anklebiter.png',
            'winter/sprite/boulder.png',
            'winter/sprite/carnivore.png',
            'winter/sprite/cowardrune.png',
            'winter/sprite/devourer.png',
            'winter/sprite/dragonpup.png',
            'winter/sprite/dynamite.png',
            'winter/sprite/firerune.png',
            'winter/sprite/gorilla.png',
            'winter/sprite/grandpa.png',
            'winter/sprite/guardrune.png',
            'winter/sprite/hellhound.png',
            'winter/sprite/hgap.png',
            'winter/sprite/ice.png',
            'winter/sprite/icecave.png',
            'winter/sprite/icechunks.png',
            'winter/sprite/kid1.png',
            'winter/sprite/kid2.png',
            'winter/sprite/kid3.png',
            'winter/sprite/powerrune.png',
            'winter/sprite/protagonist.png',
            'winter/sprite/razormane.png',
            'winter/sprite/rend.png',
            'winter/sprite/savepoint.png',
            'winter/sprite/serpent.png',
            'winter/sprite/soulreaver.png',
            'winter/sprite/strengthrune.png',
            'winter/sprite/vgap.png',
            'winter/sprite/waterrune.png',
            'winter/sprite/windrune.png',
            'winter/sprite/yeti.png',
            'winter/system_font.png',
        ]

        //const soundPaths = [
        //    'sfx/swing1.wav',
        //    'sfx/swing2.wav',
        //    'sfx/swing3.wav',
        //    'sfx/LevelUp.wav',
        //    'sfx/MenuClick.wav',
        //    'sfx/MenuBuzz.wav',
        //    'sfx/HearthRend.wav',
        //    'sfx/CrushingGale.wav',
        //    'sfx/HealingRain.wav',
        //    'sfx/MonsterHit.wav',
        //    'sfx/AnklebiterStrike.wav',
        //    //'sfx/AnklebiterHurt.wav',
        //    'sfx/AnklebiterDie.wav',
        //    'sfx/YetiHurt1.wav',
        //    'sfx/YetiHurt2.wav',
        //    'sfx/YetiHurt3.wav',
        //    'sfx/SoulReaverHurt1.wav',
        //    'sfx/SoulReaverHurt2.wav',
        //    'sfx/SoulReaverHurt3.wav',
        //    'sfx/YetiDie.wav',
        //    'sfx/SoulReaverDie.wav',
        //    'sfx/RazormaneStrike.wav',
        //    'sfx/RazormaneHurt.wav',
        //    'sfx/RazormaneDie.wav',
        //]

        const loadImage = (path: string) => {
            return new Promise<void>((resolve: ()=>void, _reject: any) => {
                const imageEl: HTMLImageElement = new Image()
                // TODO: Handle image load failure?
                imageEl.addEventListener('load', () => {
                    this.images[path] = {
                        _texture: _makeImageTexture(this.gl, imageEl),
                        width: imageEl.width,
                        height: imageEl.height,
                        yScale: 1.0,
                    }
                    resolve()
                })
                imageEl.src = path
            })
        };

        const loadJson = (path: string) => {
            return new Promise((resolve: (json:any)=>void, _reject: any) => {
                const xhr = new XMLHttpRequest()
                const onLoad = () => {
                    // TODO: Error handling?
                    const json = JSON.parse(xhr.responseText)
                    resolve(json)
                }
                xhr.addEventListener('load', onLoad)
                // TODO: Error handling?
                xhr.open('GET', path)
                xhr.send()
            })
        }

        // TODO: Actually load sound data, set up data-to-name mapping
        this.sounds = {
            slash1: new Sound(''),
            slash2: new Sound(''),
            slash3: new Sound(''),
            playerHurt: new Sound(''),
            achievement: new Sound(''),
            menuClick: new Sound(''),
            menuBuzz: new Sound(''),
            hearthRend: new Sound(''),
            crushingGale: new Sound(''),
            healingRain: new Sound(''),
            monsterHit: new Sound(''),
            anklebiterStrike: new Sound(''),
            anklebiterHurt: new Sound(''),
            anklebiterDie: new Sound(''),
            soulReaverStrike: new Sound(''),
            soulReaverHurt: new Sound(''),
            soulReaverDie: new Sound(''),
            yetiStrike: new Sound(''),
            yetiHurt: new Sound(''),
            yetiDie: new Sound(''),
            razorManeStrike: new Sound(''),
            razorManeHurt: new Sound(''),
            razorManeDie: new Sound(''),
        }

        let promises: Promise<void>[] = [
            ...imagePaths.map(loadImage),
            loadJson('winter/maps.json').then((json: any) => {
                this.maps = json
            }),
            loadJson('winter/sprites.json').then((json: any) => {
                this.sprites = json
            }),
        ]

        // TODO: Some mechanism to customize inputs
        const _KeycodeMap: {[key: string]: string} = {
            'ArrowUp': 'UP',
            'ArrowDown': 'DOWN',
            'ArrowRight': 'RIGHT',
            'ArrowLeft': 'LEFT',
            'Enter': 'ENTER',
            'Escape': 'ESCAPE',
            ' ': 'SPACE',
            'Z': 'Z',
            'z': 'Z',
            'X': 'X',
            'x': 'X',
            'C': 'C',
            'c': 'C',
            'V': 'V',
            'v': 'V',
            'B': 'B',
            'b': 'B',
            'N': 'N',
            'n': 'N',
            'M': 'M',
            'm': 'M',
        }

        const makeControlHandler = (fn: (control: Control)=>void) => {
            return (event: KeyboardEvent) => {
                if (event.defaultPrevented) {
                    return
                }
                if (!(event.key in _KeycodeMap)) {
                    return
                }
                const control = this.input.getKey(_KeycodeMap[event.key])
                fn(control)
                event.preventDefault()
            }
        }

        const onKeyDown = makeControlHandler((c: Control) => c.handleKeyDown())
        const onKeyUp = makeControlHandler((c: Control) => c.handleKeyUp())

        window.addEventListener('keydown', onKeyDown, true)
        window.addEventListener('keyup', onKeyUp, true)

        const engineRef = new PyEngine(this)
        const mainTask = engineRef.mainTask()

        const runFrame = (_timestamp: any) => {
            const {done} = mainTask.next()
            if (!done) {
                window.requestAnimationFrame(runFrame)
            } else {
                console.log("Engine done.")
            }
        }

        const startEngine = () => {
            console.log("Starting engine...")
            this.video.clearScreen()
            window.requestAnimationFrame(runFrame)
        }

        Promise.all(promises).then(startEngine)
    }

    getMapData(mapName: string): MapData {
        const mapData = this.maps[mapName]
        if (!mapData) {
            throw new Error("Map data not found")
        }
        return mapData
    }

    getImage(imagePath: string): Image {
        const image = this.images['winter/' + imagePath]
        if (!image) {
            throw new Error("Image element not found:" + imagePath)
        }
        return image
    }

    detectSpriteCollision(
        spriteName: string,
        x: number,
        y: number,
        w: number,
        h: number,
        layerIndex: number
    ): boolean {
        const sprites = this.map.spritesAt(x + 1, y + 1, w - 2, h - 2, layerIndex)
        for (let sprite of sprites) {
            if (sprite.isobs && sprite.name != spriteName) {
                return true
            }
        }
        return false
    }

    detectMapCollision(
        x: number,
        y: number,
        w: number,
        h: number,
        layerIndex: number
    ): boolean {
        const tileW = 16
        const tileH = 16
        const mapData = this.getMapData(this.map._currentMapName)
        const layer = mapData.layers[layerIndex]
        const layerWidth = layer.dimensions.width
        const layerHeight = layer.dimensions.height
        const y2 = Math.floor((y + h - 1) / tileH)
        const x2 = Math.floor((x + w - 1) / tileW)
        x = Math.floor(x / tileW)
        y = Math.floor(y / tileH)
        if (x < 0 || y < 0 || x2 >= layerWidth || y2 >= layerHeight) {
            return true
        }
        const localLayerObstructions = this.map._localLayerObstructions[layerIndex]
        for (let cy = y; cy <= y2; ++cy) {
            for (let cx = x; cx <= x2; ++cx) {
                const obsIndex = cy * layerWidth + cx
                if (obsIndex < localLayerObstructions.length) {
                    if (localLayerObstructions[obsIndex] != 0) {
                        return true
                    }
                }
            }
        }
        return false
    }
}

const FRAME_RATE = 100
const MAX_SKIP_COUNT = 10
const START_MAP = 'map01.ika-map'
const START_POS = [34 * 16, 23 * 16]

interface Spawnable {
    new (e: PyEngine, s: Sprite): Entity
}
const spawnMap: {[key: string]: Spawnable} = {
    // match each sprite name up with the associated class
    'anklebiter.ika-sprite': AnkleBiter,
    'carnivore.ika-sprite': Carnivore,
    'devourer.ika-sprite': Devourer,
    'razormane.ika-sprite': RazorMane,
    'dragonpup.ika-sprite': DragonPup,
    'hellhound.ika-sprite': HellHound,
    'yeti.ika-sprite': Yeti,
    'gorilla.ika-sprite': Gorilla,
    'soulreaver.ika-sprite': SoulReaver,

    'dynamite.ika-sprite': Dynamite,
    'waterrune.ika-sprite': WaterRune,
    'firerune.ika-sprite': FireRune,
    'windrune.ika-sprite': WindRune,
    'cowardrune.ika-sprite': CowardRune,
    'strengthrune.ika-sprite': StrengthRune,
    'powerrune.ika-sprite': PowerRune,
    'guardrune.ika-sprite': GuardRune,

    'savepoint.ika-sprite': SavePoint,

    'icecave.ika-sprite': IceWall,
    'ice.ika-sprite': IceWall,
    'icechunks.ika-sprite': IceChunks,
    'boulder.ika-sprite': Boulder,
    'vgap.ika-sprite': Gap,
    'hgap.ika-sprite': Gap,
}

class EndGameException {}

class GameLoseException extends EndGameException {}
class GameQuitException extends EndGameException {}
class GameWinException extends EndGameException {}

export class PyEngine {
    // Core engine thingie.  bleh.
    private entities: Entity[]
    private killList: Entity[]
    private things: Thing[]
    private mapThings: Thing[]
    private fields: Field[]
    private nameToEntityMap: {[key: string]: Entity}
    public player: Player | null
    private background: Image | null
    private ticksPerFrame: number
    private nextFrameTime: number
    private _engine: Engine
    public font: Font
    private mapName: string
    public fader: Crossfader
    private music: {[key: string]: Sound}
    private saveFlags: {[key: string]: string}
    private showSaveMenuAtEndOfTick: boolean
    private camera: Camera

    constructor(engine: Engine) {
        this.entities = []
        this.killList = []
        this.things = []
        this.mapThings = [] // same as this.things, but is cleared every mapSwitch
        this.fields = []

        // ika sprite "name" : Entity
        this.nameToEntityMap = {}

        this.player = null
        this.background = null

        // framerate regulating stuff:
        this.ticksPerFrame = 100.0 / FRAME_RATE
        this.nextFrameTime = 0

        this._engine = engine
        this.font = new Font(this._engine)
        this.mapName = ''

        this.fader = new Crossfader()
        // all music.  Never ever let go. (because I'm lazy)
        this.music = {
            'music/silence': new NullSound(),
        }
        this.saveFlags = {}
        this.showSaveMenuAtEndOfTick = false
        this.camera = new Camera(this)
    }

    // TODO DO NOT COMMIT - remove most of these.
    getCameraLocked() {
        return this.camera.locked
    }

    setCameraLocked(v: boolean) {
        this.camera.locked = v
    }

    getEngine() {
        return this._engine
    }

    getEntities() {
        return Object.values(this.nameToEntityMap)
    }

    getEntityForSpriteName(name: string) {
        return this.nameToEntityMap[name]
    }

    getMapName() {
        return this.mapName
    }

    hasSaveFlag(s: string) {
        return this.saveFlags.hasOwnProperty(s)
    }

    pySetBackground(img: Image) {
        this.background = img
    }

    pyUpdateCamera() {
        this.camera.update()
    }

    getPlayerEntity(): Player {
        if (this.player === null) {
            throw new Error("Expected player")
        }
        return this.player
    }

    triggerGameLose() {
        throw new GameLoseException()
    }

    triggerGameQuit() {
        throw new GameQuitException()
    }

    triggerGameWin() {
        throw new GameWinException()
    }

    getSaveFlag(s: string) {
        if (this.saveFlags.hasOwnProperty(s)) {
            return this.saveFlags[s]
        }
        return ''
    }

    setSaveFlag(s: string, v: string) {
        this.saveFlags[s] = v
    }

    setShowSaveMenuAtEndOfTick(v: boolean) {
        this.showSaveMenuAtEndOfTick = v
    }

    *mainTask() {
        const introMusic = new Sound('music/Existing.s3m')

        // TODO: Reenable
        if (showIntroLogos) {
            yield* introTask(this)
        }

        while (true) {
            this.fader.kill()
            introMusic.position = 0
            introMusic.play()
            // TODO: use return value instead.
            let resultRef: [number | null] = [null]
            const setResult = (r: number) => { resultRef[0] = r }
            yield* menuTask(this, setResult)

            if (resultRef[0] === 0) {
                introMusic.pause()
                yield* this.beginNewGameTask()
            } else if (resultRef[0] === 1) {
                introMusic.pause()
                yield* this.loadGameTask()
            } else if (resultRef[0] === 2) {
                break
            } else {
                throw new Error("Unexpected intro menu result")
            }
        }

        console.log("Exiting.") // TODO
    }

    *initTask(saveData: SaveData | null = null) {
        // clean everything
        this.killList = [...this.entities]
        this.clearKillQueue()
        this.things = []
        this.mapThings = []
        this.fields = []

        // ika sprite "name" : Entity
        this.nameToEntityMap = {}

        // TODO - redundant with map switches in beginNewGameTask/loadGameTask? (pos parameter differs...)
        if (saveData !== null) {
            // evil
            yield* this.mapSwitchTask(saveData.mapName, null, false)
        } else {
            yield* this.mapSwitchTask(START_MAP, null, false)
        }

        if (this.player === null) {
            this.player = new Player(this)
        }
        this.addEntity(this.player)

        if (saveData !== null) {
            this.player.sprite.x = saveData.playerX
            this.player.sprite.y = saveData.playerY
            this.player.sprite.layer = saveData.playerLayer
            this.player.stats = saveData.stats.clone()
            this.saveFlags = {...saveData.flags}
        } else {
            [this.player.sprite.x, this.player.sprite.y] = START_POS
            const name = this._engine.map.getMetaData()['entityLayer']
            const layer = this._engine.map.findLayerByName(name)
            if (layer === null) {
                throw new Error("Unrecognized layer name")
            }
            this.player.sprite.layer = layer
        }

        this.things.push(new HPBar(this))
        this.things.push(new MPBar(this))
        this.things.push(new EXPBar(this))

        this.camera = new Camera(this)
        this.camera.center()
        this.things.push(this.camera)
    }

    *beginNewGameTask() {
        this.saveFlags = {}
        yield* sceneTask(this, 'intro')
        yield* this.mapSwitchTask(START_MAP, START_POS, false)
        yield* this.initTask()

        // insanely inefficient:
        const startImages = createBlurImages(this)
        this.draw()
        const endImages = createBlurImages(this)
        yield* blurFadeTask(this, 50, startImages, endImages)
        freeBlurImages(this, startImages)
        freeBlurImages(this, endImages)
        yield* this.runTask()
    }

    readSaves() {
        const saves = []
        let index = 0
        while (true) {
            const save = loadGame(index)
            if (save === null) {
                return saves
            }
            saves.push(save)
            index += 1
        }
    }

    writeSave(index: number) {
        saveGame(index, new SaveData(
            this.getPlayerEntity().stats.clone(),
            {...this.saveFlags},
            this.mapName,
            this.getPlayerEntity().sprite.x,
            this.getPlayerEntity().sprite.y,
            this.getPlayerEntity().sprite.layer
        ))
    }

    *loadGameTask() {
        let result: SaveData[] = []
        const setResult = (s: SaveData | null) => {
            if (s === null) {
                return
            }
            result = [s]
        }
        yield* loadMenuTask(this, setResult)
        if (result.length > 0) {
            const startImages = createBlurImages(this)
            this.saveFlags = {}
            const pos = [result[0].playerX, result[0].playerY, result[0].playerLayer]
            yield* this.mapSwitchTask(result[0].mapName, pos, false)
            yield* this.initTask(result[0])
            this.draw()
            const endImages = createBlurImages(this)
            yield* blurFadeTask(this, 50, startImages, endImages)
            freeBlurImages(this, startImages)
            freeBlurImages(this, endImages)
            yield* this.runTask()
        }
    }

    getImage(key: string) {
        return this._engine.getImage(key)
    }

    *mapSwitchTask(mapName: string, dest: number[] | null = null, fade: boolean = true) {
        console.log("switching to map " + mapName)
        let startImages: Image[] | null = null
        if (fade) {
            this.draw()
            startImages = createBlurImages(this)
        }

        this.mapName = mapName

        this.background = null
        this.mapThings = []
        this.fields = []

        const currentMapName = mapName.replace('.ika-map', '')
        this._engine.map.load(currentMapName)

        const mapScript = mapScripts[currentMapName]
        mapScript.autoexec(this)

        const metaData = this._engine.map.getMetaData()

        this.readZones(mapScript)
        this.readEnts()
        if (this.player) {
            this.player.setState(this.player.defaultState())
        }
        if (dest && this.player) {
            if (dest.length === 2) {
                [this.player.sprite.x, this.player.sprite.y] = dest
                const lay = this._engine.map.findLayerByName(metaData['entityLayer'])
                if (lay === null) {
                    throw new Error("Unrecognized layer name")
                }
                this.player.sprite.layer = lay
            } else if (dest.length === 3) {
                [this.player.sprite.x, this.player.sprite.y, this.player.sprite.layer] = dest
            }

            this.camera.center()
        }

        if (metaData.hasOwnProperty('music')) {
            this.playMusic('music/' + metaData['music'])
        }

        if (fade) {
            if (startImages === null) {
                throw new Error("Unexpected null startImages")
            }
            this.draw()
            const endImages = createBlurImages(this)
            yield* blurFadeTask(this, 50, startImages, endImages)
            freeBlurImages(this, startImages)
            freeBlurImages(this, endImages)
        }

        this.synchTime()
    }

    *warpTask(dest: [number, number]) {
        this.draw()
        const startImage = this._engine.video.grabImage(0, 0, this._engine.video.xres, this._engine.video.yres)

        const p = this.getPlayerEntity()
        p.direction = Direction.Down
        p.setState(p.defaultState())
        p.startAnimation('stand')
        p.animate()

        p.sprite.x = dest[0]
        p.sprite.y = dest[1]
        this.camera.center()

        this.draw()
        const endImage = this._engine.video.grabImage(0, 0, this._engine.video.xres, this._engine.video.yres)

        const time = 50
        const endTime = this.getTime() + time
        let now = this.getTime()
        while (now < endTime) {
            const opacity = (endTime - now) / time
            this._engine.video.blit(endImage, 0, 0)
            this._engine.video.tintBlit(startImage, 0, 0, opacity)
            this._engine.video.showPage()
            yield null
            now = this.getTime()
        }

        this._engine.video.freeImage(startImage)
        this._engine.video.freeImage(endImage)
        this.synchTime()
    }

    *runTask() {
        try {
            let skipCount = 0
            this.nextFrameTime = this.getTime() + this.ticksPerFrame
            while (1) {
                const t = this.getTime()

                // if we're ahead, delay
                if (t < this.nextFrameTime) {
                    yield* delayTask(Math.floor(this.nextFrameTime - t))
                }

                if (this._engine.controls.cancel()) {
                    yield* this.pauseTask()
                }

                // Do some thinking
                yield* this.tickTask()

                // if we're behind, and can, skip the frame.  else draw
                if (t > this.nextFrameTime && skipCount < MAX_SKIP_COUNT) {
                    skipCount += 1
                } else {
                    skipCount = 0
                    this.draw()
                    this._engine.video.showPage()
                    yield null
                }

                this.nextFrameTime += this.ticksPerFrame
            }
        } catch (e) {
            if (e instanceof GameLoseException) {
                yield* this.gameOverTask()
                this.killList = [...this.entities]
                this.clearKillQueue()
            } else if (e instanceof GameWinException) {
                yield* fadeOutTask(this, 200, this.draw.bind(this))
                this.killList = [...this.entities]
                this.clearKillQueue()
                yield* creditsTask(this)
            } else if (e instanceof GameQuitException) {
                this.killList = [...this.entities]
                this.clearKillQueue()
            } else {
                throw e
            }
        }
    }

    draw() {
        if (this.background) {
            this._engine.video.scaleBlit(this.background, 0, 0, this._engine.video.xres, this._engine.video.yres)
        }
        this._engine.map.render()

        for (let t of this.things) {
            t.draw()
        }
        for (let t of this.mapThings) {
            t.draw()
        }
    }

    *tickTask() {
        // We let ika do most of the work concerning sprite movement.
        // (in particular, collision detection)
        this._engine.map.processSprites()

        // update entities
        for (let ent of this.entities) {
            ent.update()
        }
        this.clearKillQueue()

        // check fields
        const p = this.getPlayerEntity()
        const rlayer = p.sprite.layer
        const rx = p.sprite.x
        const ry = p.sprite.y
        const rw = p.sprite.hotwidth
        const rh = p.sprite.hotheight
        for (let f of this.fields) {
            if (f.test(rlayer, rx, ry, rw, rh)) {
                const scriptTask = f.scriptTask
                yield* scriptTask(this)
                break
            }
        }

        // update Things.
        // for each thing in each thing list, we update.
        // If the result is true, we delete the thing, else
        // move on.
        for (let t of [this.things, this.mapThings]) {
            let i = 0
            while (i < t.length) {
                const result = t[i].update()

                if (result) {
                    t.splice(i, 1)
                } else {
                    i += 1
                }
            }
        }

        if (this.showSaveMenuAtEndOfTick) {
            this.showSaveMenuAtEndOfTick = false

            yield* fadeOutTask(this, 50, this.draw.bind(this))
            this.draw()
            yield* saveMenuTask(this)
            yield* fadeInTask(this, 50, this.draw.bind(this))
            this.synchTime()
        }
    }

    addEntity(ent: Entity) {
        this.entities.push(ent)
        this.nameToEntityMap[ent.sprite.name] = ent
    }

    destroyEntity(ent: Entity) {
        ent.sprite.x = -1000
        ent.sprite.y = -1000
        ent.stop()
        this.killList.push(ent)
    }

    addMapThing(thing: Thing) {
        this.mapThings.push(thing)
    }

    addThing(thing: Thing) {
        this.things.push(thing)
    }

    readZones(mapScript: MapScript) {
        // Read all the zones on the map, and create fields.
        this.fields = []

        for (let i = 0; i < this._engine.map.layercount; ++i) {
            const zones = this._engine.map.getZones(i)
            for (let [x, y, w, h, scriptTaskName] of zones) {
                const scriptTask = mapScript.fns[scriptTaskName]
                this.fields.push(new Field([x,y,w,h], i, scriptTask))
            }
        }
    }

    readEnts() {
        // Grabs all entities from the map, and adds them to the engine.

        // making a gamble here: assuming all entities except the player are tied to the map
        if (this.player) {
            this.clearKillQueue()
            for (let e of this.entities) {
                if (e !== this.player) {
                    this.killList.push(e)
                }
            }
            this.clearKillQueue()
        }

        for (let sprite of Object.values(this._engine.map.sprites)) {
            const spawnable = spawnMap[sprite.spritename]
            if (spawnable !== undefined) {
                this.addEntity(new spawnable(this, sprite))
            } else if (sprite.spritename !== PLAYER_SPRITE) {
                console.log(`Unknown entity sprite {sprite.spritename}  Ignoring.`)
            }
        }
    }

    clearKillQueue() {
        // it's a bad idea to tweak the entity list in the middle of an iteration,
        // so we queue them up, and nuke them here.
        for (let ent of this.killList) {
            if (ent === this.player) {
                this.player = null
            }
            ent.sprite.x = -100
            ent.sprite.y = 0
            ent.sprite.stop()
            delete this.nameToEntityMap[ent.sprite.name]
            this._engine.map.removeSprite(ent.sprite)
            // brython workaround?
            this.entities = this.entities.filter(e => e.sprite.name !== ent.sprite.name)
        }

        this.killList = []
    }

    getTime() {
        return this._engine.getTime()
    }

    synchTime() {
        // Used to keep the engine from thinking it has to catch up er
        // executing an event or something.

        this.nextFrameTime = this.getTime()
    }

    *gameOverTask() {
        const c = new Caption(this, this.font, 'G A M E   O V E R', null, Math.floor((this._engine.video.yres - this.font.height) / 2), 1000000)
        const t = 80
        let i = 0
        this.fields = []
        while (true) {
            i = Math.min(i + 1, t)
            c.update()
            yield* this.tickTask()
            this.draw()

            // darken the screen, draw the game over message:
            const o = i / t
            this._engine.video.drawRect(0, 0, this._engine.video.xres, this._engine.video.yres, 0, 0, 0, o)
            c.draw()

            this._engine.video.showPage()
            yield* delayTask(4)

            if (i === t && this._engine.controls.attack()) {
                break
            }
        }
    }

    *pauseTask() {
        this.draw()
        const s = new PauseScreen(this)
        yield* s.runTask()

        this.synchTime()
    }

    playMusic(fname: string) {
        let m: Sound
        if (this.music.hasOwnProperty(fname)) {
            m = this.music[fname]
        } else {
            m = new Sound(fname)
            m.loop = true
            this.music[fname] = m
        }

        this.fader.reset(m)
        if (!this.things.includes(this.fader)) {
            this.things.push(this.fader)
        }
    }
}

// loading code:

function main() {
    const removeChildren = (node : HTMLElement) => {
        while (node.firstChild) {
            node.removeChild(node.firstChild)
        }
    }
    removeChildren(document.body)

    const engine = new Engine()
    engine.run()
}

main()
