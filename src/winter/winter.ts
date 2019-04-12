
import { Animator, makeAnim, makeAnimRange } from "./animator.js"
;(window as any).animator = { Animator, makeAnim, makeAnimRange }

import { Caption } from "./caption.js"
;(window as any).caption = { Caption }

import { Direction, invert, fromDelta, toDelta } from "./Direction.js"
;(window as any).Dir = {
    Left: Direction.Left,
    Right: Direction.Right,
    Up: Direction.Up,
    Down: Direction.Down,
    UpLeft: Direction.UpLeft,
    UpRight: Direction.UpRight,
    DownLeft: Direction.DownLeft,
    DownRight: Direction.DownRight,

    fromDelta,
    invert,
    toDelta,
}

import {
    AttribWindow,
    MagicWindow,
    MenuWindow,
    SaveLoadMenu,
    ScrollableTextFrame,
    StatWindow,
    TextFrame,
} from "./gui.js"
;(window as any).gui = {
    AttribWindow,
    MagicWindow,
    MenuWindow,
    SaveLoadMenu,
    ScrollableTextFrame,
    StatWindow,
    TextFrame,
}

import { blurFadeTask, createBlurImages, fadeInTask, fadeOutTask, freeBlurImages } from "./effects.js"
;(window as any).effects = { blurFadeTask, createBlurImages, fadeInTask, fadeOutTask, freeBlurImages }

import { Entity } from "./entity.js"
;(window as any).entity = { Entity }

import { Field } from "./field.js"
;(window as any).field = { Field }

import { introTask, menuTask } from "./intro.js"
;(window as any).intro = { introTask, menuTask }

import { Player, PLAYER_SPRITE } from "./player.js"
;(window as any).player = { Player, PLAYER_SPRITE }

import { loadGame, SaveData, saveGame } from "./saveload.js"
;(window as any).saveload = { loadGame, SaveData, saveGame }

import { StatSet } from "./statset.js"
;(window as any).statset = { StatSet }

import { wrapText } from "./wraptext.js"
;(window as any).wraptext = { wrapText }

;(window as any).hasProperty = (obj: any, name: string) => {
    return obj.hasOwnProperty(name) && obj[name] !== undefined
}

interface Size {
    width: number
    height: number
}

export class Point {
    x: number
    y: number
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

export class Input {
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
    ) {
    }
}

export const RGB = (r: number, g: number, b: number, a: number): number => {
    return ((
        ((r | 0) & 0xff)
        | (((g | 0) & 0xff) << 8)
        | (((b | 0) & 0xff) << 16)
        | (((a | 0) & 0xff) << 24)
    ) >>> 0)
}
(window as any).RGB = RGB

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

    Stop() {
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
            this.Stop()
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
            this.Stop()
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

export class FontClass {
    height: number

    constructor(
        private _engine: Engine,
    ) {
        this.height = 10
    }

    // TODO: Other members?

    CenterPrint(x: number, y: number, text: string) {
        this.Print(x - this.StringWidth(text) / 2 , y, text)
    }

    StringWidth(s: string): number {
        let w = 0
        for (let glyph of this._genGlyphs(s)) {
            w += glyph.width
        }
        return w
    }

    PrintWithOpacity(x: number, y: number, text: string, opacity: number) {
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

    Print(x: number, y: number, text: string) {
        this.PrintWithOpacity(x, y, text, 1.0)
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
(window as any).FontClass = FontClass

class MapClass {
    private _xwin: number
    private _ywin: number
    private _localLayerDatas: number[][]
    // TODO: Make private?
    _localLayerObstructions: number[][]
    _currentMapName: string
    private _spriteID: number
    // TODO: make private and provide different accessor?
    sprites: {[key: string]: Sprite}
    mapSpriteNames_: string[]
    layercount: number

    constructor(
        private _engine: Engine,
        private _video: VideoClass
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

    Render() {
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

            for (let [_, sprite] of layerSprites[i]) {
                // This game doesn't seem to use custom renderscripts

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

    SetTile(x: number, y: number, layerIndex: number, tileIndex: number) {
        const mapData = this._engine.getMapData(this._currentMapName)
        const layer = mapData.layers[layerIndex]
        const localLayerData = this._localLayerDatas[layerIndex]
        const index = y * layer.dimensions.width + x
        localLayerData[index] = tileIndex
    }

    SetObs(x: number, y: number, layerIndex: number, obs: number) {
        const mapData = this._engine.getMapData(this._currentMapName)
        const layer = mapData.layers[layerIndex]
        const localLayerObstructions = this._localLayerObstructions[layerIndex]
        const index = y * layer.dimensions.width + x
        localLayerObstructions[index] = obs
    }

    Switch(path: string) {
        this.clearSprites()

        this._currentMapName = path.replace('maps/', '').replace('.ika-map', '')
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

    GetMetaData() {
        const mapData = this._engine.getMapData(this._currentMapName)
        return mapData.information.meta
    }

    GetZones(layerIndex: number) {
        let zoneTuples = []
        const mapData = this._engine.getMapData(this._currentMapName)

        for (let zone of mapData.layers[layerIndex].zones) {
            let scriptName = null
            for (let zoneMetadata of mapData.zones) {
                if (zoneMetadata.label === zone.label) {
                    scriptName = zoneMetadata.script
                    break
                }
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

    FindLayerByName(name: string): number | null {
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
    clearSprites() {
        for (let name of this.mapSpriteNames_) {
            delete this.sprites[name]
        }
        this.mapSpriteNames_ = []
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
(window as any).MapClass = MapClass

interface SpriteData {
    width: number
    height: number
    count: number
    hotspotX: number
    hotspotY: number
    hotspotWidth: number
    hotspotHeight: number
}

class Sound {
    position: number = 0.0
    volume: number = 1.0
    loop: boolean = false

    constructor(
        _name: string
    ) {}

    play() {}
    pause() {}
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

class VideoClass {
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

    Blit(image: Image, x: number, y: number) {
        this.TintScaleBlit(image, x, y, image.width, image.height, 1.0)
    }

    ClearScreen() {
        const engine = this._getEngine()
        const gl = engine.gl
        engine.targetPageFramebuffer()
        gl.clearColor(0, 0, 0, 1.0)
        gl.clear(gl.COLOR_BUFFER_BIT)
    }

    DrawRect(x1: number, y1: number, x2: number, y2: number, color: number) {
        const engine = this._getEngine()
        engine.targetPageFramebuffer()
        const r = (color & 0xff) / 255.0
        const g = ((color >> 8) & 0xff) / 255.0
        const b = ((color >> 16) & 0xff) / 255.0
        const a = ((color >> 24) & 0xff) / 255.0
        engine.drawRect(x1, y1, x2 - x1 + 1, y2 - y1 + 1, r, g, b, a)
    }

    GrabImage(x1: number, y1: number, x2: number, y2: number) {
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

    FreeImage(image: Image) {
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

    ScaleBlit(image: Image, x: number, y: number, width: number, height: number) {
        this.TintScaleBlit(image, x, y, width, height, 1.0)
    }

    ShowPage() {
        const engine = this._getEngine()
        engine.targetCanvasFramebuffer()
        engine.drawImage(engine.pageImage, 0, 0, engine.pageImage.width, engine.pageImage.height, 0, 0, engine.pageImage.width, engine.pageImage.height, 1.0)

        // Makes compositing more reliable.  Some maps don't draw the whole screen.
        this.ClearScreen()
    }

    TintBlit(image: Image, x: number, y: number, alpha: number) {
        this.TintScaleBlit(image, x, y, image.width, image.height, alpha)
    }

    TintScaleBlit(image: Image, x: number, y: number, width: number, height: number, alpha: number) {
        const engine = this._getEngine()
        engine.targetPageFramebuffer()
        engine.drawImage(image, 0, 0, image.width, image.height, x, y, width, height, alpha)
    }

    // TODO other members...
}
(window as any).VideoClass = VideoClass

export interface PyEngine {
    addThing: (thing: any)=>void
    getCameraLocked: ()=>boolean
    getEngine: ()=>{js: Engine}
    getEntityForSpriteName: (name: string)=>{js: Entity}
    getPlayerEntity: ()=>{js: Entity}
    getSaveFlag: (s: string) => string | undefined
    pyDestroyEntity: (entity: Entity)=>void
    pyGivePlayerXP: (xp: number)=>void
    font: {js: FontClass}
    player: {js: {stats: StatSet}}
    saveFlags: undefined | {$jsobj: undefined | {[key: string]: string}}
    setCameraLocked: (locked: boolean)=>void
    setSaveFlag: (s: string, v: string) => void
    triggerGameLose: ()=>void
}

export interface Controls {
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
        this.engine = engineRef.getEngine().js
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
        this.engine.drawSnow(this.time, this.count, this.vx, this.vy, this.r, this.g, this.b)
    }
}
;(window as any).Snow = Snow

export function *delayTask(time: number) {
    const targetEnd = Date.now() + (time * 10)
    // Busy waiting, sort of... :(
    while (targetEnd > Date.now()) {
        yield null
    }
}
;(window as any).delayTask = delayTask

export function random(low: number, high: number) {
    return Math.floor(Math.random() * (high - low)) + low
}
;(window as any).random = random

export function hypot(x: number, y: number) {
    return Math.sqrt(x * x + y * y)
}
;(window as any).hypot = hypot

export class Engine {
    maps: {[key: string]: MapData}
    images: {[key: string]: Image}
    sprites: {[key: string]: SpriteData}
    sounds: {[key: string]: Sound}
    width: number
    height: number
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
    video: VideoClass

    constructor() {
        this.images = {}
        this.maps = {}
        this.sprites = {}
        this.sounds = {}
        this.input = new Input()
        this.video = new VideoClass(this)
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

    run(taskFn: ()=>boolean) {
        this.startMsec = Date.now()
        this.width = 320
        this.height = 240

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
            //'winter/gfx/ui/divider.png',
            //'winter/gfx/ui/font.png',
            //'winter/gfx/ui/font2.png',
            'winter/gfx/ui/icon_att.png',
            'winter/gfx/ui/icon_mag.png',
            'winter/gfx/ui/icon_mres.png',
            'winter/gfx/ui/icon_pres.png',
            //'winter/gfx/ui/icon_speed.png',
            //'winter/gfx/ui/item_dynamite.png',
            //'winter/gfx/ui/item_sword.png',
            //'winter/gfx/ui/meter.png',
            'winter/gfx/ui/pointer.png',
            //'winter/gfx/ui/rune_apoplexy.png',
            //'winter/gfx/ui/rune_quicken.png',
            //'winter/gfx/ui/rune_shield.png',
            //'winter/gfx/ui/rune_squall.png',
            //'winter/gfx/ui/rune_strike.png',
            //'winter/gfx/ui/rune_surge.png',
            //'winter/gfx/ui/rune_trinity.png',
            //'winter/gfx/ui/text_attributes.png',
            //'winter/gfx/ui/text_equip.png',
            //'winter/gfx/ui/text_exp.png',
            //'winter/gfx/ui/text_hp.png',
            //'winter/gfx/ui/text_items.png',
            //'winter/gfx/ui/text_lvl.png',
            //'winter/gfx/ui/text_menu.png',
            //'winter/gfx/ui/text_mp.png',
            //'winter/gfx/ui/text_spells.png',
            //'winter/gfx/ui/text_stats.png',
            //'winter/gfx/ui/win2_background.png',
            //'winter/gfx/ui/win2_bottom.png',
            //'winter/gfx/ui/win2_bottom_left.png',
            //'winter/gfx/ui/win2_bottom_right.png',
            //'winter/gfx/ui/win2_right.png',
            //'winter/gfx/ui/win2_top.png',
            //'winter/gfx/ui/win2_top_left.png',
            //'winter/gfx/ui/win2_top_right.png',
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
                        _texture: _makeImageTexture(gl, imageEl),
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

        const runFrame = (_timestamp: any) => {
            if (taskFn()) {
                window.requestAnimationFrame(runFrame)
            } else {
                console.log("Engine done.")
            }
        }

        const startEngine = () => {
            console.log("Starting engine...")
            this.video.ClearScreen()
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
(window as any).Engine = Engine

// loading code:

const removeChildren = (node : HTMLElement) => {
    while (node.firstChild) {
        node.removeChild(node.firstChild)
    }
}

const addPythonScript = (path : string) => {
    const s = document.createElement('script')
    s.type = 'text/python'
    s.src = path
    document.body.appendChild(s)
}

const enum BrythonDebugLevel {
    None = 0,
    ShowErrors = 1,
    Translate = 2,
    TranslateAll = 10,
}

interface BrythonOptions {
    debug: BrythonDebugLevel
}

declare var brython: (options: BrythonOptions) => void

removeChildren(document.body)

addPythonScript('system.py')
brython({
    debug: BrythonDebugLevel.ShowErrors,
})
