
interface FlakeState {
    x: number
    y: number
    vx: number
    life: number
}

class WinterSnow {
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
(window as any).WinterSnow = WinterSnow

interface Size {
    width: number
    height: number
}

class Point {
    x: number
    y: number
}

interface Input {
    getKey(key: string): Control
}

interface Control {
    _pressed: number
    _position: number
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

interface Image {
    _el: HTMLImageElement | HTMLCanvasElement
    width: number
    height: number
}

class Canvas {
    constructor(
        public width: number,
        public height: number,
        public _el: HTMLCanvasElement,
        public _ctx: CanvasRenderingContext2D,
    ) {
    }
}

const RGB = (r: number, g: number, b: number, a: number): number => {
    return (
        (Math.floor(r) & 0xff)
        | ((Math.floor(g) & 0xff) << 8)
        | ((Math.floor(b) & 0xff) << 16)
        | ((Math.floor(a) & 0xff) << 24)
    )
}
(window as any).RGB = RGB

const _RGBAToCSS = (colorValue: number): string => {
    const r = colorValue & 0xff
    const g = (colorValue >> 8) & 0xff
    const b = (colorValue >> 16) & 0xff
    const a = ((colorValue >> 24) & 0xff) / 255.0
    return "rgba(" + r + ", " + g + ", " + b + ", " + a + ")"
}

const _makeCanvasAndContext = (width: number, height: number): [HTMLCanvasElement, CanvasRenderingContext2D] => {
    const el = window.document.createElement('canvas')
    el.width = width
    el.height = height
    const ctx = el.getContext('2d')
    if (ctx === null) {
        throw new Error("Couldn't get 2D context")
    }
    ctx.mozImageSmoothingEnabled = false
    ctx.webkitImageSmoothingEnabled = false
    // TypeScript doesn't know about msImageSmoothingEnabled...
    //ctx.msImageSmoothingEnabled = false
    ctx.imageSmoothingEnabled = false
    // We maintain one pristine state on the stack for resetting
    // clipping.
    ctx.save()
    return [el, ctx]
}

class Entity {
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

    MoveTo(x: number, y: number) {
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

    Update() {
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
            this._Move(newDir)
        }
    }

    private _MoveDiagonally(d: string): string {
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

    private _Move(newDir: string) {
        const moveDir = this._MoveDiagonally(newDir)
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
            || (this.entobs && engine.detectEntityCollision(this.name, x, y, this.hotwidth, this.hotheight, this.layer))
        )
    }

    Touches(otherEnt: Entity): boolean {
        const x1 = this.x
        const y1 = this.y
        const w = this.hotwidth
        const h = this.hotheight

        if (x1     > otherEnt.x + otherEnt.hotwidth ||
            y1     > otherEnt.y + otherEnt.hotheight ||
            x1 + w < otherEnt.x ||
            y1 + h < otherEnt.y)
        {
            return false
        } else {
            return true
        }
    }
}

class FontClass {
    private height: number

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
        const ctx = this._engine.ctx
        ctx.save()
        ctx.globalAlpha = opacity / 255.0
        this.Print(x, y, text)
        ctx.restore()
    }

    Print(x: number, y: number, text: string) {
        const imageEl = this._engine.getImageEl('system_font.png')
        let cursorX = Math.floor(x)
        let cursorY = Math.floor(y)
        for (let glyph of this._genGlyphs(text)) {
            this._engine.ctx.drawImage(
                imageEl,
                glyph.tileX,
                glyph.tileY,
                glyph.width,
                glyph.height,
                cursorX,
                cursorY,
                glyph.width,
                glyph.height)
            cursorX += glyph.width
        }
    }

    *_genGlyphs(text:string) {
        const subsets = this._engine.systemFontData.subsets
        const widths = this._engine.systemFontData.widths
        const heights = this._engine.systemFontData.heights
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
    entities: {[key: string]: Entity}
    mapEntityNames_: string[]
    layercount: number

    constructor(
        private _engine: Engine,
        private _video: VideoClass
    ) {
        this._spriteID = 0
        this.entities = {}
        this.mapEntityNames_ = []
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
        const layerEnts: [number, Entity][][] = []
        for (let i = 0; i < layerCount; ++i) {
            layerEnts.push([])
        }
        // TODO: Better way to do this in typescript?  For..of something?
        for (let key in this.entities) {
            const ent = this.entities[key]
            layerEnts[ent.layer].push([ent.y, ent])
        }
        for (let layerEnt of layerEnts) {
            layerEnt.sort()
        }

        // This game only uses a single tile map:
        const imageEl = this._engine.getImageEl('snowy.png')

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
                    const tileX = (tileIndex % tilesPerRow) * tileW
                    const tileY = Math.floor(tileIndex / tilesPerRow) * tileH
                    this._engine.ctx.drawImage(
                        imageEl,
                        tileX,
                        tileY,
                        tileW,
                        tileH,
                        x * tileW - adjustX,
                        y * tileH - adjustY,
                        tileW,
                        tileH
                    )
                }
            }

            for (let [_, ent] of layerEnts[i]) {
                // This game doesn't seem to use custom renderscripts

                const spritePath = 'sprite/' + ent.spritename.replace('.ika-sprite', '.png')
                const spriteImageEl = this._engine.getImageEl(spritePath)

                const frameIndex = Math.max(0, ent.specframe)
                const frameX = (frameIndex % 8) * ent.spritewidth
                const frameY = Math.floor(frameIndex / 8) * ent.spriteheight

                // This game doesn't use sprite visibility toggling.
                this._engine.ctx.drawImage(
                    spriteImageEl,
                    frameX,
                    frameY,
                    ent.spritewidth,
                    ent.spriteheight,
                    ent.x - ent.hotx - xw,
                    ent.y - ent.hoty - yw,
                    ent.spritewidth,
                    ent.spriteheight
                )
            }
        }
        // TODO: Hookretrace?
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
        this.clearMapEntities()

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
                const ent = new Entity(
                    entity.x,
                    entity.y,
                    i,
                    entity.sprite,
                    entity.label,
                    spriteData,
                    this._engine,
                )
                this.entities[ent.name] = ent
                this.mapEntityNames_.push(ent.name)
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

    // Adding some methods to replace direct access of python dict...
    addEntity(x: number, y: number, layer: number, spritename: string) {
        this._spriteID += 1
        const name = "sprite_" + this._spriteID
        const spriteData = this._engine.sprites[spritename]
        const ent = new Entity(x, y, layer, spritename, name, spriteData, this._engine)
        this.entities[ent.name] = ent
        return ent
    }
    RemoveEntity(entity: Entity) {
        delete this.entities[entity.name]
    }
    clearMapEntities() {
        for (let name of this.mapEntityNames_) {
            delete this.entities[name]
        }
        this.mapEntityNames_ = []
    }
    EntitiesAt(x: number, y: number, width: number, height: number, layer: number) {
        const x2 = x + width
        const y2 = y + height

        const found = []
        for (let key in this.entities) {
            const ent = this.entities[key]
            if (ent.layer != layer) {
                continue
            }
            if (x > ent.x + ent.hotwidth) {
                continue
            }
            if (y > ent.y + ent.hotheight) {
                continue
            }
            if (x2 < ent.x) {
                continue
            }
            if (y2 < ent.y) {
                continue
            }
            found.push(ent)
        }
        return found
    }
    ProcessEntities() {
        const _TIME_RATE = 100
        for (let key in this.entities) {
            const ent = this.entities[key]
            ent._speedCount += ent.speed
            while (ent._speedCount >= _TIME_RATE) {
                ent.Update()
                ent._speedCount -= _TIME_RATE
            }
        }
    }
}
(window as any).MapClass = MapClass

interface SystemFontData {
    subsets: number[][]
    widths: number[]
    heights: number[]
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

class VideoClass {
    // Resolution used in this game...
    readonly xres = 320
    readonly yres = 240
    //colours = None // TODO
    // TODO: Only necessary to hide cyclical reference from Brython:
    private _getEngine: ()=>Engine

    constructor(
        engine: Engine,
    ) {
        this._getEngine = ()=>engine
    }

    private _assertBlendmodeSupported(blendmode?: number) {
        const Opaque = 0
        const Matte = 1
        //AlphaBlend = 2
        //AddBlend = 3
        //SubtractBlend = 4
        //MultiplyBlend = 5
        //PreserveBlend = 6

        if (blendmode !== undefined && blendmode != Opaque && blendmode != Matte) {
            throw new Error("Unsupported blendmode") // TODO: Handle more complicated blendmodes.
        }
    }

    Blit(image: Image, x: number, y: number, blendmode?: number) {
        // Theoretically, we should be discarding the alpha channel of anything
        // that we blit as "opaque", but it's likely that any such graphics
        // already lack an alpha channel.
        this._assertBlendmodeSupported(blendmode)
        this._getEngine().ctx.drawImage(image._el, x, y)
    }

    ClearScreen() {
        this._getEngine().ctx.fillStyle = 'rgb(0, 0, 0)'
        this._getEngine().ctx.fillRect(0, 0, this._getEngine().width, this._getEngine().height)
    }

    ResetClipScreen() {
        // Pop and immediately save pristine state
        this._getEngine().ctx.restore()
        this._getEngine().ctx.save()
    }

    ClipScreen(left?: number, top?: number, right?: number, bottom?: number) {
        // TODO: Migrate empty param calls to ResetClipScreen() instead.
        this.ResetClipScreen()
        if (left !== undefined && top !== undefined && right !== undefined && bottom !== undefined) {
            this._getEngine().ctx.rect(left, top, right - left, bottom - top)
            this._getEngine().ctx.clip()
        }
    }

    DrawPixel(x: number, y: number, colour: number, blendmode?: number) {
        this._assertBlendmodeSupported(blendmode)
        this._getEngine().ctx.fillStyle = _RGBAToCSS(colour)
        this._getEngine().ctx.fillRect(x, y, 1, 1)
    }

    DrawRect(x1: number, y1: number, x2: number, y2: number, colour: number, fill: boolean, blendmode?: number) {
        this._assertBlendmodeSupported(blendmode)
        if (fill) {
            this._getEngine().ctx.fillStyle = _RGBAToCSS(colour)
            // TODO: Maybe check on negative dimension behavior?
            this._getEngine().ctx.fillRect(x1, y1, x2 - x1 + 1, y2 - y1 + 1)
        } else {
            throw new Error("unfilled DrawRect not implemented") // TODO
        }
    }

    GrabImage(x1: number, y1: number, x2: number, y2: number) {
        const width = x2 - x1
        const height = y2 - y1
        var canvasEl
        var ctx
        ;[canvasEl, ctx] = _makeCanvasAndContext(width, height)
        ctx.drawImage(this._getEngine().canvasEl, -x1, -y1)
        return new Canvas(width, height, canvasEl, ctx)
    }

    ScaleBlit(image: Image, x: number, y: number, width: number, height: number, blendmode?: number) {
        this._assertBlendmodeSupported(blendmode)
        this._getEngine().ctx.drawImage(image._el, 0, 0, image.width, image.height, x, y, width, height)
    }

    ShowPage() {
        this._getEngine().displayCtx.drawImage(this._getEngine().canvasEl, 0, 0)
        // Pretty sure any clipping gets reset here...
        //this.ClipScreen()
    }

    TintBlit(image: Image, x: number, y: number, tintColor: number, blendMode?: number) {
        // TODO: actually only need alpha -- we only otherwise use white
        this._getEngine().ctx.save()
        this._getEngine().ctx.globalAlpha = ((tintColor >> 24) & 0xff) / 255.0
        this.Blit(image, x, y, blendMode)
        this._getEngine().ctx.restore()
    }

    TintDistortBlit(image: Image, upLeft: any, _upRight: any, downRight: any, _downLeft: any, blendmode?: number) {
        // TODO: We actually only use TintDistortBlit as a version of ScaleBlit
        // with alpha.
        this._getEngine().ctx.save()
        const tintColor: number = upLeft[2]
        this._getEngine().ctx.globalAlpha = ((tintColor >> 24) & 0xff) / 255.0
        this.ScaleBlit(
            image,
            upLeft[0],
            upLeft[1],
            downRight[0] - upLeft[0],
            downRight[1] - upLeft[1],
            blendmode)
        this._getEngine().ctx.restore()
    }

    DrawTriangle(v1: any, v2: any, v3: any) {
        // TODO: We actually only use DrawTriangle in the credits scene, to
        // draw a gradiated black triangle.
        const ctx = this._getEngine().ctx

        const dx = v3[0] - v2[0]
        const dy = v3[1] - v2[1]
        const len = Math.sqrt(dx * dx + dy * dy)
        const ndx = dx / len
        const ndy = dy / len

        const dx1 = v1[0] - v2[0]
        const dy1 = v1[1] - v2[1]
        const projLen = dx1 * ndx + dy1 * ndy
        const projx = ndx * projLen
        const projy = ndy * projLen

        const x2 = dx1 - projx
        const y2 = dy1 - projy

        const gradientEndX = v1[0] - x2
        const gradientEndY = v1[1] - y2
        const gradient = ctx.createLinearGradient(v1[0], v1[1], gradientEndX, gradientEndY)
        gradient.addColorStop(0, 'rgb(0, 0, 0)')
        gradient.addColorStop(1, 'rgb(0, 0, 0, 0)')

        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.moveTo(v1[0], v1[1])
        ctx.lineTo(v2[0], v2[1])
        ctx.lineTo(v3[0], v3[1])
        ctx.fill()
    }

    // TODO other members...
}
(window as any).VideoClass = VideoClass

class Engine {
    maps: {[key: string]: MapData}
    imageEls: {[key: string]: HTMLImageElement}
    sprites: {[key: string]: SpriteData}
    width: number
    height: number
    startMsec: number
    systemFontData: SystemFontData
    canvasEl: HTMLCanvasElement
    ctx: CanvasRenderingContext2D
    displayCanvasEl: HTMLCanvasElement
    displayCtx: CanvasRenderingContext2D
    map: MapClass
    _video: VideoClass

    constructor(
        private _getKey: (key: string) => Control,
    ) {
        this.imageEls = {}
        this.maps = {}
        this.sprites = {}
        this._video = new VideoClass(this)
        this.map = new MapClass(this, this._video)
    }

    run(
        taskFn: ()=>boolean,
        mapsPath: string,
        spritesPath: string,
        imagePaths: string[],
        systemFontData: SystemFontData
    ) {
        this.startMsec = Date.now()
        this.width = 320
        this.height = 240
        this.systemFontData = systemFontData

        ;[this.canvasEl, this.ctx] = _makeCanvasAndContext(this.width, this.height)
        ;[this.displayCanvasEl, this.displayCtx] = _makeCanvasAndContext(this.width, this.height)

        // Typescript doesn't know about imageRendering yet.
        const style = this.displayCanvasEl.style as any
        style.border = "1px solid"
        style.imageRendering = "pixelated"
        style.imageRendering = "optimizeSpeed"
        style.imageRendering = "-moz-crisp-edges"
        style.imageRendering = "-webkit-optimize-contrast"
        style.width = "" + this.width * 2
        style.height = "" + this.height * 2
        style.display = "block"
        style.marginLeft = "auto"
        style.marginRight = "auto"
        window.document.body.appendChild(this.displayCanvasEl)
        window.document.body.style.backgroundColor = "#dddddd"

        let promises: Promise<void>[] = []
        for (let path of imagePaths) {
            const loadImage = (resolve: ()=>void, _reject: any) => {
                const imageEl = window.document.createElement('img')
                // TODO: Handle image load failure?
                imageEl.addEventListener('load', resolve)
                imageEl.src = path
                this.imageEls[path] = imageEl

                // TODO: Not sure what's going on, but for some reason it seems
                // adding the image element to the page with a non-none display
                // is a prerequisite to having its width and height properties
                // populated, even after waiting for the load event, contrary to
                // all documentation seen online.  Observed in Chrome 59,
                // Firefox 54.
                imageEl.style.position = "absolute"
                imageEl.style.top = "0"
                imageEl.style.left = "0"
                imageEl.style.opacity = "0"
                window.document.body.appendChild(imageEl)
            }
            promises.push(new Promise(loadImage))
        }

        const loadJson = (path: string) => {
            const fn = (resolve: (json:any)=>void, _reject: any) => {
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
            }
            return new Promise(fn)
        }

        const setMapJson = (json: any) => {
            this.maps = json
        }

        const setSpriteJson = (json: any) => {
            this.sprites = json
        }

        promises.push(loadJson(mapsPath).then(setMapJson))
        promises.push(loadJson(spritesPath).then(setSpriteJson))

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

        const onKeyDown = (event: KeyboardEvent) => {
            if (event.defaultPrevented) {
                return
            }
            if (!(event.key in _KeycodeMap)) {
                return
            }
            const control = this._getKey(_KeycodeMap[event.key])
            control._pressed = 1
            control._position = 1
            event.preventDefault()
        }

        const onKeyUp = (event: KeyboardEvent) => {
            if (event.defaultPrevented) {
                return
            }
            if (!(event.key in _KeycodeMap)) {
                return
            }
            const control = this._getKey(_KeycodeMap[event.key])
            control._position = 0
            event.preventDefault()
        }

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

    getImageEl(imagePath: string): HTMLImageElement {
        const imageEl = this.imageEls['winter/' + imagePath]
        if (!imageEl) {
            throw new Error("Image element not found:" + imagePath)
        }
        return imageEl
    }

    getImage(imagePath: string): Image {
        const el = this.getImageEl(imagePath)
        return {
            _el: el,
            width: el.width,
            height: el.height,
        }
    }

    detectEntityCollision(
        entName: string,
        x: number,
        y: number,
        w: number,
        h: number,
        layerIndex: number
    ): boolean {
        const ents = this.map.EntitiesAt(x, y, w, h, layerIndex)
        for (let ent of ents) {
            if (ent.isobs && ent.name != entName) {
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
addPythonScript('main.py')
brython({
    debug: BrythonDebugLevel.ShowErrors,
})
