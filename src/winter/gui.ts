import { Engine, FontClass, Image, PyEngine } from "./winter.js";

import { SaveData } from "./saveload.js";

class ImageCursor {
    private engine: Engine
    private image: Image

    constructor(
        engineRef: PyEngine,
        imageKey: string,
    ) {
        this.engine = engineRef.getEngine().js
        this.image = this.engine.getImage(imageKey)
    }

    getWidth() { return this.image.width }
    getHeight() { return this.image.height }

    draw(x: number, y: number) {
        const hotspotX = this.image.width
        const hotspotY = (this.image.height / 2) | 0
        this.engine.video.Blit(this.image, x - hotspotX, y - hotspotY)
    }
}

export class Widget {
    // Basic GUI element class.  By itself, the Widget is an invisible container.
    // While this may be useful in and of itself, widgets probably won't see much
    // direct use.  Subclasses are where the action usually is.

    protected engine: Engine
    children: Widget[]
    private border: number

    constructor(
        engineRef: PyEngine,
        protected x: number = 0,
        protected y: number = 0,
        protected width: number = 0,
        protected height: number = 0,
    ) {
        this.engine = engineRef.getEngine().js
        this.children = []
        this.border = 0
    }

    setX(value: number) { this.x = value }
    setY(value: number) { this.y = value }
    getX() { return this.x }
    getY() { return this.y }

    setWidth(value: number) {
        if (value <= 0) { throw new Error("Width must be positive!") }
        this.width = value
    }
    getWidth() { return this.width }

    setHeight(value: number) {
        if (value <= 0) { throw new Error("Height must be positive!") }
        this.height = value
    }
    getHeight() { return this.height }

    getRight() { return this.x + this.width }
    setRight(value: number) { this.x = value - this.width }

    getBottom() { return this.y + this.height }
    setBottom(value: number) { this.y = value - this.height }

    getPosition(): [number, number] { return [this.x, this.y] }
    setPosition(value: [number, number]) {
        this.setX(value[0])
        this.setY(value[1])
    }

    getBorder() { return this.border }
    setBorder(value: number) { this.border = value }

    dockTop() {
        this.setY(this.getBorder())
        return this
    }

    dockBottom() {
        this.setBottom(this.engine.height - this.getBorder())
        return this
    }

    dockLeft() {
        this.setX(this.getBorder())
        return this
    }

    dockRight() {
        this.setRight(this.engine.width - this.getBorder())
        return this
    }

    draw(xofs = 0, yofs = 0) {
        // Draws the widget onscreen.  xofs and yofs are added to the widget's own positional coordinates.
        // xofs and yofs are customarily the absolute x/y position of the containing widget, if any.
        this.children.forEach(child => child.draw(xofs + this.x, yofs + this.y))
    }

    addChild(child: Widget) {
        this.children.push(child)
    }
    setChildren(children: Widget[]) {
        this.children = children
    }

    autoSize() {
        // Sets the size of the frame such that every child will be visibly contained within it.
        this.width = 1
        this.height = 1
        this.children.forEach(child => {
            this.width = Math.max(this.width, child.getWidth() + child.getX())
            this.height = Math.max(this.height, child.getHeight() + child.getY())
        })
    }

    layout() {}
}

class Layout extends Widget {
    constructor(
        engineRef: PyEngine,
        children: Widget[] = [],
        protected pad: number = 0,
    ) {
        super(engineRef)
        this.setChildren(children)
    }

    // TODO: Try using relative offset for children?
    setX(value: number) {
        this.children.forEach(child => {
            child.setX(child.getX() + value - this.getX())
        })
        super.setX(value)
    }

    setY(value: number) {
        this.children.forEach(child => {
            child.setY(child.getY() + value - this.getY())
        })
        super.setY(value)
    }

    draw(xoffset = 0, yoffset = 0) {
        this.children.forEach(child => {
            child.draw(xoffset, yoffset)
        })
    }
}

class VerticalBoxLayout extends Layout {
    // Arranges its children in a vertical column.

    layout() {
        let y = this.y
        this.children.forEach(child => {
            child.layout()
            child.setPosition([this.x, y])
            y += child.getHeight() + this.pad
        })

        this.width = Math.max(...this.children.map(c => c.getWidth())) - this.x
        this.height = y - this.y - this.pad
    }
}

class HorizontalBoxLayout extends Layout {
    // Arranges its children in a horizontal row.

    layout() {
        let x = this.x
        this.children.forEach(child => {
            child.layout()
            child.setPosition([x, this.y])
            x += child.getWidth() + this.pad
        })

        this.width = x - this.x
        this.height = Math.max(...this.children.map(c => c.getHeight())) - this.y
    }
}

class FlexGridLayout extends Layout {
    // More robust GridLayout.  Each row/column is as big as it needs to be.  No
    // bigger.

    constructor(
        engineRef: PyEngine,
        private cols: number,
        children: Widget[] = [],
    ) {
        super(engineRef, children, 0)
    }

    layout() {
        this.children.forEach(child => {
            child.layout()
        })

        // Create a 2D matrix to hold widgets for each column
        const cols: Widget[][] = []
        for (let i = 0 ; i < this.cols; ++i) { cols.push([]) }
        this.children.forEach((child, i) => {
            cols[i % this.cols].push(child)
        })

        // Get the widest child in each column
        const rowWidths = cols.map(col =>
            Math.max(...col.map(cell => cell.getWidth() + this.pad))
        )

        // Get the tallest child in each row
        const getRowHeight = (col: Widget[], rowIndex: number) =>
            (rowIndex >= col.length) ? 0 : col[rowIndex].getHeight() + this.pad
        const colHeights = cols[0].map((_, rowIndex) =>
            Math.max(...cols.map(col => getRowHeight(col, rowIndex)))
        )

        let [row, col, x, y] = [0, 0, 0, 0]
        this.children.forEach(child => {
            child.setPosition([x + this.x, y + this.y])
            x += rowWidths[col]
            col += 1
            if (col >= this.cols) {
                ;[x, y] = [0, y + colHeights[row]]
                ;[row, col] = [row + 1, 0]
            }
        })

        this.width = Math.max(...this.children.map(child => child.getRight())) - this.pad - this.x
        this.height = Math.max(...this.children.map(child => child.getBottom())) - this.pad - this.y
    }
}

class Frame extends Widget {
    // A widget that appears as a graphical frame of some sort.
    // Frames are most commonly used as container widgets.

    private iTopleft: Image
    private iTopright: Image
    private iBottomleft: Image
    private iBottomright: Image
    private iLeft: Image
    private iRight: Image
    private iTop: Image
    private iBottom: Image
    private iCentre: Image
    leftWidth: number

    constructor(
        engineRef: PyEngine,
        x: number = 0,
        y: number = 0,
        width: number = 0,
        height: number = 0,
    ) {
        super(engineRef, x, y, width, height)
        this.iTopleft = this.engine.getImage('gfx/ui/win_top_left.png')
        this.iTopright = this.engine.getImage('gfx/ui/win_top_right.png')
        this.iBottomleft = this.engine.getImage('gfx/ui/win_bottom_left.png')
        this.iBottomright = this.engine.getImage('gfx/ui/win_bottom_right.png')
        this.iLeft = this.engine.getImage('gfx/ui/win_left.png')
        this.iRight = this.engine.getImage('gfx/ui/win_right.png')
        this.iTop = this.engine.getImage('gfx/ui/win_top.png')
        this.iBottom = this.engine.getImage('gfx/ui/win_bottom.png')
        this.iCentre = this.engine.getImage('gfx/ui/win_background.png')
        this.leftWidth = this.iLeft.width
    }

    draw(xofs = 0, yofs = 0) {
        const x = this.x + xofs
        const y = this.y + yofs
        const x2 = x + this.width
        const y2 = y + this.height

        this.engine.video.Blit(this.iTopleft,  x - this.iTopleft.width, y - this.iTopleft.height)
        this.engine.video.Blit(this.iTopright, x2, y - this.iTopright.height)
        this.engine.video.Blit(this.iBottomleft, x - this.iBottomleft.width, y2)
        this.engine.video.Blit(this.iBottomright, x2, y2)

        this.engine.video.ScaleBlit(this.iLeft, x - this.iLeft.width, y, this.iLeft.width, y2 - y)
        this.engine.video.ScaleBlit(this.iRight, x2, y, this.iRight.width, y2 - y)

        this.engine.video.ScaleBlit(this.iTop, x, y - this.iTop.height, x2 - x, this.iTop.height)
        this.engine.video.ScaleBlit(this.iBottom, x, y2, x2 - x, this.iBottom.height)

        this.engine.video.ScaleBlit(this.iCentre, x, y, x2 - x, y2 - y)

        super.draw(xofs, yofs)
    }
}

class Picture extends Widget {
    private image: Image

    constructor(
        engineRef: PyEngine,
        imageKey: string,
    ) {
        super(engineRef)
        this.image = this.engine.getImage(imageKey)
        this.setWidth(this.image.width)
        this.setHeight(this.image.height)
    }

    draw(xofs = 0, yofs = 0) {
        this.engine.video.ScaleBlit(this.image, this.x + xofs, this.y + yofs, this.width, this.height)
    }
}

class StaticText extends Widget {
    // A widget that appears as some lines of text.
    // No frame is drawn.

    public font: FontClass

    constructor(
        engineRef: PyEngine,
        protected text: string[] = [],
        x: number = 0,
        y: number = 0,
        width: number = 0,
        height: number = 0,
    ) {
        super(engineRef, x, y, width, height)
        this.font = engineRef.font.js
        this.autoSize()
    }

    getText() { return this.text }
    setText(value: string[]) { this.text = value.slice(0) }

    addText(text: string[]) { this.text = [...this.text, ...text] }
    clear() { this.text = [] }

    autoSize() {
        if (this.text.length) {
            const widths = this.text.map(s => this.font.StringWidth(s))
            this.setWidth(Math.max(...widths))
            this.setHeight(this.text.length * this.font.height)
        } else {
            this.setWidth(1)
            this.setHeight(1)
        }
    }

    draw(xofs: number, yofs: number) {
        const x = this.x + xofs
        let y = this.y + yofs
        this.text.forEach(s => {
            this.font.Print(x, y, s)
            y += this.font.height
        })
        super.draw(xofs, yofs)
    }
}

class ScrollableTextLabel extends StaticText {
    // A text label that can potentially hold more text than it can visually display, given
    // whatever size it may be at the time.

    // The text label's scroll position (YWin) is in pixel coordinates, and can range from 0 to
    // its YMax value.

    private ywin: number
    private ymax: number

    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
        this.ywin = 0
        this.ymax = 0
    }

    getYWin() { return this.ywin }
    setYWin(value: number) {
        this.ywin = Math.min(this.ymax - this.height, value)
        this.ywin = Math.max(this.ywin, 0)
    }

    setText(value: string[]) {
        super.setText(value)
        this.ymax = this.text.length * this.font.height
    }

    addText(text: string[]) {
        super.addText(text)
        this.ymax = this.text.length * this.font.height
    }

    draw(xoffset = 0, yoffset = 0) {
        const x = this.x + xoffset
        const y = this.y + yoffset

        const firstLine = Math.max(0, (this.ywin / this.font.height) | 0)
        const lastLine = Math.min(this.text.length, (((this.height + this.ywin) / this.font.height) | 0) + 1)

        let curY = y - this.ywin % this.font.height
        for (let i = firstLine; i < lastLine; ++i) {
            const line = this.text[i]
            this.font.Print(x, curY, line)
            curY += this.font.height
        }
    }
}

export class TextFrame extends Frame {
    // A frame with text in it.  This is a simple convenience class, combining the
    // Frame and StaticText controls into a single convenient object.

    private text: StaticText

    constructor(
        engineRef: PyEngine,
        text: string[] = [],
    ) {
        super(engineRef)
        this.text = new StaticText(engineRef, text)

        this.addChild(this.text)
        this.autoSize()
    }

    getText() { return this.text.getText() }
    setText(text: string[]) { this.text.setText(text) }

    addText(text: string[]) { this.text.addText(text) }

    autoSize() {
        this.text.autoSize()
        this.setWidth(this.text.getWidth())
        this.setHeight(this.text.getHeight())
    }
}

export class ScrollableTextFrame extends Frame {
    // Simple combination of ScrollableTextLabel and Frame
    // Most of the work here is making the class behave both like a ScrollableTextLabel and
    // a Frame at the same time.

    private text: ScrollableTextLabel
    public font: FontClass

    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
        this.text = new ScrollableTextLabel(engineRef)
        this.font = this.text.font
        this.addChild(this.text)
    }

    getYWin() { return this.text.getYWin() }
    setYWin(value: number) { this.text.setYWin(value) }
    getText() { return this.text.getText() }
    setText(value: string[]) { this.text.setText(value) }

    addText(text: string[]) { this.text.addText(text) }

    autoSize() {
        this.text.autoSize()
        this.setWidth(this.text.getWidth())
        this.setHeight(this.text.getHeight())
    }
}

class SaveGameFrame extends Frame {
    constructor(
        engineRef: PyEngine,
        icons: {[key: string]: Picture},
        save: SaveData,
    ) {
        super(engineRef)
        const layout = new VerticalBoxLayout(engineRef)
        this.addChild(layout)

        const padStr = (n: number, s: string): string => s.length >= n ? s : padStr(n - 1, '0' + s)
        const pad = (n: number, v: number): string => padStr(n, "" + v)
        const stats = save.stats
        layout.setChildren([
            new HorizontalBoxLayout(engineRef, [
                new StaticText(engineRef, [`HP${pad(3, stats.hp)}/${pad(3, stats.maxhp)}`]),
                new Widget(engineRef, 0, 0, 16, 0),
                new StaticText(engineRef, [`Lv. ${pad(2, stats.level)}`])
            ]),
            new FlexGridLayout(engineRef, 4, [
                icons['att'], new StaticText(engineRef, [`${pad(2, stats.att)}  `]),
                icons['mag'], new StaticText(engineRef, [`${pad(2, stats.mag)}  `]),
                icons['pres'], new StaticText(engineRef, [`${pad(2, stats.pres)}  `]),
                icons['mres'], new StaticText(engineRef, [`${pad(2, stats.mres)}  `]),
            ])
        ])

        layout.layout()
        this.autoSize()
    }
}

export class SaveLoadMenu {
    private engine: Engine
    private cursor: ImageCursor
    private layout: VerticalBoxLayout
    private cursorPos: number = 0
    private oldY: number = 0
    private curY: number = 0
    private wndHeight: number = 0
    private lastTime: number = 0

    constructor(
        engineRef: PyEngine,
        saves: SaveData[],
        saving: boolean = false,
    ) {
        this.engine = engineRef.getEngine().js

        const icons: {[key: string]: Picture} = {}
        ;['att', 'mag', 'pres', 'mres'].forEach(s => {
            icons[s] = new Picture(engineRef, `gfx/ui/icon_${s}.png`)
        })

        this.cursor = new ImageCursor(engineRef, 'gfx/ui/pointer.png')

        const boxes = saves.map(s => new SaveGameFrame(engineRef, icons, s))
        if (saving) {
            boxes.push(new TextFrame(engineRef, ['Create New']))
        } else if (boxes.length == 0) {
            boxes.push(new TextFrame(engineRef, ['No Saves']))
        }

        this.layout = new VerticalBoxLayout(engineRef, boxes, 16)
        this.layout.layout()

        if (boxes.length > 0) {
            this.wndHeight = this.layout.children[0].getHeight() + 16
        } else {
            // What should we do here?
        }

        this.layout.setX(16) // doesn't change
    }

    draw() {
        this.layout.setY(Math.floor((this.engine.height - this.wndHeight) / 2 - this.oldY + 16))
        this.layout.draw()
        this.cursor.draw(16, Math.floor(this.engine.height / 2)) // cursor doesn't move, everything else does
    }

    update(): number | string | null {
        const now = this.engine.getTime()
        const delta = Math.min(100, now - this.lastTime)
        this.lastTime = now

        if (this.curY < this.oldY) {
            this.oldY = Math.max(this.curY, this.oldY - 2 * delta)
        } else if (this.curY > this.oldY) {
            this.oldY = Math.min(this.curY, this.oldY + 2 * delta)
        } else {
            if (this.engine.controls.up() && this.cursorPos > 0) {
                this.cursorPos -= 1
                this.curY = this.cursorPos * this.wndHeight
            } else if (this.engine.controls.down() && this.cursorPos < this.layout.children.length - 1) {
                this.cursorPos += 1
                this.curY = this.cursorPos * this.wndHeight
            } else if (this.engine.controls.attack()) {
                return this.cursorPos
            } else if (this.engine.controls.cancel()) {
                return 'cancel'
            }
        }
        return null
    }
}

class SubScreenWindow extends Frame {
    protected layoutObj: Layout
    // TODO: eliminate:
    protected engineRef: PyEngine

    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
        this.engineRef = engineRef
        this.layoutObj = this.createLayout(engineRef)
        this.addChild(this.layoutObj)
        this.setBorder(this.leftWidth)
    }

    protected createLayout(engineRef: PyEngine) {
        return new VerticalBoxLayout(engineRef)
    }

    update() {
        this.layoutObj.setChildren(this.createContents())
        this.layoutObj.layout()
        this.autoSize()
    }

    createContents(): Widget[] {
        return []
    }
}

export class StatWindow extends SubScreenWindow {
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
    }

    createContents(): Widget[] {
        const stats = this.engineRef.player.js.stats
        const padStr = (n: number, s: string): string => s.length >= n ? s : padStr(n - 1, '0' + s)
        const pad = (n: number, v: number): string => padStr(n, "" + v)
        return [
            new StaticText(this.engineRef, ['Level ' + pad(2, stats.level)]),
            new StaticText(this.engineRef, ['Exp']),
            new StaticText(this.engineRef, [' ' + pad(6, stats.exp) + '/']),
            new StaticText(this.engineRef, ['  ' + pad(6, stats.next)]),
            // expbar thingie goes here
            new StaticText(this.engineRef, ['HP']),
            new StaticText(this.engineRef, [' ' + pad(3, stats.hp) + '/' + pad(3, stats.maxhp)]),
            // hp bar
            new StaticText(this.engineRef, ['MP']),
            new StaticText(this.engineRef, [' ' + pad(3, stats.mp) + '/' + pad(3, stats.maxmp)]),
            // mp bar
        ]
    }
}

export class AttribWindow extends SubScreenWindow {
    private icons: {[key: string]: Picture}

    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
        this.icons = {}
        ;['att', 'mag', 'pres', 'mres'].forEach(s => {
            this.icons[s] = new Picture(engineRef, `gfx/ui/icon_${s}.png`)
        })
    }

    protected createLayout(engineRef: PyEngine) {
        return new FlexGridLayout(engineRef, 2)
    }

    createContents(): Widget[] {
        const padStr = (n: number, s: string): string => s.length >= n ? s : padStr(n - 1, '0' + s)
        const pad = (n: number, v: number): string => padStr(n, "" + v)
        const stats = this.engineRef.player.js.stats
        return [
            this.icons['att'], new StaticText(this.engineRef, ['...' + pad(3, stats.att)]),
            this.icons['mag'], new StaticText(this.engineRef, ['...' + pad(3, stats.mag)]),
            this.icons['pres'], new StaticText(this.engineRef, ['...' + pad(3, stats.pres)]),
            this.icons['mres'], new StaticText(this.engineRef, ['...' + pad(3, stats.mres)])
        ]
    }
}

export class MagicWindow extends SubScreenWindow {
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
    }

    protected createLayout(engineRef: PyEngine) {
        return new VerticalBoxLayout(engineRef)
    }

    createContents(): Widget[] {
        const txt = ['Magic:']
        const addIfFlag = (name: string, text: string) => {
            if (this.engineRef.saveFlags !== undefined
                && this.engineRef.saveFlags.$jsobj !== undefined
                && this.engineRef.saveFlags.$jsobj[name] !== undefined) {
                txt.push(text)
            }
        }
        addIfFlag('firerune', 'Z...Hearth Rend')
        addIfFlag('windrune', 'X...Crushing Gale')
        addIfFlag('waterrune', 'C...Healing Rain')
        addIfFlag('cowardrune', 'B...Shiver')
        return [new StaticText(this.engineRef, txt)]
    }
}

export class MenuWindow extends Widget {
    protected textCtrl: ScrollableTextFrame
    private cursor: ImageCursor
    private cursorY: number
    private cursorPos: number
    private cursorSpeed: number
    // A menu.  A list of textual options displayed in some sort of text container,
    // with a cursor that responds to user input, allowing the user to select an option.

    // I'll readily admit that this is somewhat limiting.  Doing a SoM style ring menu with
    // this class is not very realistic, but it could be implemented as its own class. (and
    // probably should, considering how different it is from this.
    constructor(
        engineRef: PyEngine,
    ) {
        super(engineRef)
        this.textCtrl = new ScrollableTextFrame(engineRef)
        this.cursor = new ImageCursor(engineRef, 'gfx/ui/pointer.png')
        this.cursorY = 0
        this.cursorPos = 0
        this.cursorSpeed = 2 // speed at which the cursor moves (in pixels per update)
        this.addChild(this.textCtrl)

        this.addText([
            'Resume',
            //'Controls',
            //'Load Game',
            'Exit'
        ])
        this.autoSize()
        this.setBorder(this.textCtrl.leftWidth)
    }

    getWidth() { return this.width }
    setWidth(value: number) {
        this.width = value
        this.textCtrl.setWidth(value - this.cursor.getWidth())
    }

    getHeight() { return this.height }
    setHeight(value: number) {
        this.height = value
        this.textCtrl.setHeight(value)
    }

    getText() { return this.textCtrl.getText() }
    setText(value: string[]) { this.textCtrl.setText(value) }

    getBorder() { return this.textCtrl.getBorder() }
    setBorder(value: number) { this.textCtrl.setBorder(value) }

    addText(text: string[]) { this.textCtrl.addText(text) }

    autoSize() {
        const w = this.cursor.getWidth()
        this.textCtrl.setPosition([w, 0])
        this.textCtrl.autoSize()
        this.setWidth(this.textCtrl.getWidth() + w)
        this.setHeight(this.textCtrl.getHeight())
    }

    update(): number | string | null {
        // Performs one tick of menu input.  This includes scrolling things around, and updating
        // the position of the cursor, based on user interaction.

        // If the user has selected an option, then the return value is the index of that option.
        // If the user hit the cancel (ESC) key, the Cancel object is returned.
        // else, None is returned, to signify that nothing has happened yet.
        let cy = this.cursorY
        // TODO: handle it the manly way, by making the cursor repeat after a moment

        // update the cursor
        const fontHeight = this.textCtrl.font.height

        const delta = this.cursorPos * fontHeight - this.textCtrl.getYWin() - cy
        if (delta > 0) {
            if (cy < this.textCtrl.getHeight() - fontHeight) {
                this.cursorY += this.cursorSpeed
            } else {
                this.textCtrl.setYWin(this.textCtrl.getYWin() + this.cursorSpeed)
            }
        } else if (delta < 0) {
            if (cy > 0) {
                this.cursorY -= this.cursorSpeed
            } else if (this.textCtrl.getYWin() > 0) {
                this.textCtrl.setYWin(this.textCtrl.getYWin() - this.cursorSpeed)
            }
        } else {
            // Maybe this isn't a good idea.  Maybe it is.
            // only move the cursor if delta is zero
            // that way movement doesn't get bogged
            // down by a cursor that moves too slowly
            if (this.engine.controls.up() && this.cursorPos > 0) {
                this.cursorPos -= 1
            } else if (this.engine.controls.down() && this.cursorPos < this.getText().length - 1) {
                this.cursorPos += 1
            } else if (this.engine.controls.enter()) {
                return this.cursorPos
            } else if (this.engine.controls.cancel()) {
                return 'cancel'
            }
        }
        return null
    }

    draw(xoffset = 0, yoffset = 0) {
        this.textCtrl.draw(this.x + xoffset, this.y + yoffset)
        const fontHeight = this.textCtrl.font.height
        this.cursor.draw(
            this.x + this.textCtrl.getX() + xoffset,
            this.y + this.textCtrl.getY() + yoffset + this.cursorY + Math.floor(fontHeight / 2)
        )
    }
}
