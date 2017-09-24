from browser import window

Opaque = 0
Matte = 1
AlphaBlend = 2
AddBlend = 3
SubtractBlend = 4
MultiplyBlend = 5
PreserveBlend = 6

#def Delay(time):
#    raise RuntimeError("Use DelayTask instead.")

_TIME_RATE = 100

def DelayTask(time):
    targetEnd = window.Date.now() + (time * 10)
    # Busy waiting, sort of... :(
    while targetEnd > window.Date.now():
        yield None

def Exit():
    pass # TODO

def GetCanvasEl():
    global _engine
    return _engine.canvasEl

def GetRGB(colorValue):
    r = colorValue & 0xff
    g = (colorValue >> 8) & 0xff
    b = (colorValue >> 16) & 0xff
    a = ((colorValue >> 24) & 0xff)
    return (r, g, b, a)

def GetTime():
    global _engine
    deltaMsec = window.Date.now() - _engine.startMsec
    return (deltaMsec // 10)

def ProcessEntities():
    global _engine
    global Map
    for ent in Map.entities.values():
        ent._speedCount += ent.speed
        while ent._speedCount >= _TIME_RATE:
            ent.Update()
            ent._speedCount -= _TIME_RATE

def Random(low, high):
    return window.Math.floor(window.Math.random() * (high - low)) + low

def RGB(r, g, b, a = 255):
    return (
        (int(r) & 0xff)
        | ((int(g) & 0xff) << 8)
        | ((int(b) & 0xff) << 16)
        | ((int(a) & 0xff) << 24)
    )

def _RGBAToCSS(colorValue):
    r = colorValue & 0xff
    g = (colorValue >> 8) & 0xff
    b = (colorValue >> 16) & 0xff
    a = ((colorValue >> 24) & 0xff) / 255.0
    return "rgba(" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ")"

class _ControlClass(object):
    def __init__(self):
        self._pressed = 0
        self._position = 0

    def Pressed(self):
        p = self._pressed
        self._pressed = 0
        return p

    def Position(self):
        return self._position

class _KeyboardClass(object):
    def __init__(self):
        self._keys = {}

    def __getitem__(self, key):
        if key not in self._keys:
            self._keys[key] = _ControlClass()
        return self._keys[key]

    # TODO other members...

class _JoystickClass(object):
    def __init__(self):
        self.axes = []
        self.reverseAxes = []
        self.buttons = []

    # TODO other members...

class _Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Entity(object):
    def __init__(self, x, y, layer, spritename):
        self.x = x
        self.y = y

        self.destLocation = _Point(x, y)
        self.destVector = _Point(0, 0)

        # Theoretically, we should turn these members into properties and do
        # stuff when the client changes them, but the game in question does not
        # modify them.
        self.layer = layer
        self.spritename = spritename

        self.specframe = -1
        self.name = None
        self.movescript = None

        self.speed = 100
        self.isobs = True
        self.mapobs = True
        self.entobs = True

        spriteData = _engine.sprites[spritename]

        self.spritewidth = spriteData.width
        self.spriteheight = spriteData.height
        self.hotx = spriteData.hotspotX
        self.hoty = spriteData.hotspotY
        self.hotwidth = spriteData.hotspotWidth
        self.hotheight = spriteData.hotspotHeight

        self._speedCount = 0

    def __hash__(self):
        # Hashability workaround
        return id(self)

    def Update(self):
        pass

    def Stop(self):
        self.destLocation.x = self.x
        self.destLocation.y = self.y
        self.destVector.x = 0
        self.destVector.y = 0
        self.isMoving = False
        # This game doesn't seem to use idlescript

class Font(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self.height = 10

    # TODO other members...
    def StringWidth(self, s):
        global _engine
        w = 0
        subset = _engine.systemFontData['subsets'][0]
        widths = _engine.systemFontData['widths']
        for ch in s:
            if ch in ['\n', '\t', '~']:
                raise NotImplementedError() # TODO
            index = subset[ord(ch)]
            w += widths[index] + 1
        return w

    def Print(self, x, y, text):
        global _engine
        imageEl = _engine.getImageEl('system_font.png')
        cursorX = x
        cursorY = y
        subset = _engine.systemFontData['subsets'][0]
        widths = _engine.systemFontData['widths']
        heights = _engine.systemFontData['heights']
        for (i, ch) in enumerate(text):
            if ch in ['\n', '\t', '~']:
                raise NotImplementedError() # TODO
            index = subset[ord(ch)]
            w = widths[index] + 1
            h = heights[index]
            tileX = (index % 16) * 9
            tileY = (index // 16) * 10
            _engine.ctx.drawImage(imageEl, tileX, tileY, w, h, cursorX, cursorY, w, h)
            cursorX += w

class Canvas(object):
    def __init__(self, width, height, el, ctx):
        self.width = width
        self.height = height
        self._el = el
        self._ctx = ctx

class Image(object):
    def __init__(self, init_arg):
        global _engine
        if isinstance(init_arg, str):
            self._path = init_arg
            self._el = _engine.getImageEl(self._path)
            self.width = self._el.width
            self.height = self._el.height
        else:
            raise NotImplementedError() # TODO: Also handle case where first arg is a canvas?

    # TODO other members...

class _InputClass(object):
    def __init__(self):
        self.keyboard = _KeyboardClass()
        self.joysticks = [_JoystickClass()]

        # Not sure this is a good idea...
        self.up = self.keyboard['UP']
        self.down = self.keyboard['DOWN']
        self.left = self.keyboard['LEFT']
        self.right = self.keyboard['RIGHT']
        self.enter = self.keyboard['ENTER']
        self.cancel = self.keyboard['ESCAPE']

    #@staticmethod
    #def Update():
    #    raise RuntimeError("Use UpdateTask instead.")

    @staticmethod
    def UpdateTask():
        # Input update is automatic, but Input.Update() is used to signify
        # waiting for the next frame.
        # TODO: We can probably consolidate any DelayTask calls...
        yield None

    # TODO other members...

Input = _InputClass()

class _MapClass(object):
    def __init__(self):
        self.entities = {}
        self._currentMapName = None
        self._xwin = 0
        self._ywin = 0
        self.layercount = None

    @property
    def xwin(self):
        return self._xwin

    @xwin.setter
    def xwin(self, value):
        self._setCamera(value, self.ywin)

    @property
    def ywin(self):
        return self._ywin

    @ywin.setter
    def ywin(self, value):
        self._setCamera(self.xwin, value)

    def _setCamera(self, x, y):
        global _engine
        global Video
        mapData = _engine.maps[self._currentMapName]
        dimensions = mapData.header.dimensions
        width = dimensions.width
        height = dimensions.height
        if width > 0:
            self._xwin = max(0, min(x, width - Video.xres - 1))
        else:
            self._xwin = x

        if height > 0:
            self._ywin = max(0, min(y, height - Video.yres - 1))
        else:
            self._ywin = y

    def Render(self):
        global _engine
        global Video
        mapData = _engine.maps[self._currentMapName]

        # This game only uses the single tile map with this fixed size:
        tileW = 16
        tileH = 16
        tilesPerRow = 16

        layerEnts = [[] for x in mapData.layers]
        for ent in self.entities.values():
            layerEnts[ent.layer].append((ent.y, ent))
        for ents in layerEnts:
            ents.sort()

        # This game only uses a single tile map:
        imageEl = _engine.getImageEl('snowy.png')

        # SetCameraTarget (and SetPlayer, which calls it) are not used by the
        # game.
        #
        # SetRenderList is not used by the game.
        for (i, layer) in enumerate(mapData.layers):
            # This game doesn't use layer position
            xw = (self._xwin * layer.parallax.mulx // layer.parallax.divx)
            yw = (self._ywin * layer.parallax.muly // layer.parallax.divy)
            firstX = xw // tileW
            firstY = yw // tileH
            adjustX = xw % tileW
            adjustY = yw % tileH
            # This game doesn't use wrapped layers.

            w = layer.dimensions.width
            h = layer.dimensions.height
            lenX = (Video.xres + tileW - 1) // tileW
            lenY = (Video.yres + tileH - 1) // tileH + 1

            if firstX < 0:
                lenX -= -firstX
                adjustX += firstX * tileW
                firstX = 0
            if firstY < 0:
                lenY -= -firstY
                adjustY += firstY * tileH
                firstY = 0
            if firstX + lenX > w:
                lenX = w - firstX
            if firstY + lenY > h:
                lenY = h - firstY

            for y in range(lenY):
                for x in range(lenX):
                    index = (firstY + y) * w + (firstX + x)
                    # This game doesn't use tile animations
                    tileIndex = layer.data[index]
                    tileX = (tileIndex % tilesPerRow) * tileW
                    tileY = (tileIndex // tilesPerRow) * tileH
                    _engine.ctx.drawImage(
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

            for (_, ent) in layerEnts[i]:
                # This game doesn't seem to use custom renderscripts

                spritePath = 'sprite/' + ent.spritename[:-len('.ika-sprite')] + '.png'
                spriteImageEl = _engine.getImageEl(spritePath)

                frameIndex = max(0, ent.specframe)
                frameX = (frameIndex % 8) * ent.spritewidth
                frameY = (frameIndex // 8) * ent.spriteheight

                # This game doesn't use sprite visibility toggling.
                _engine.ctx.drawImage(
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

    def Switch(self, path):
        global _engine
        self.entities = {}

        assert path.startswith('maps/')
        assert path.endswith('.ika-map')
        self._currentMapName = path[len('maps/'):-len('.ika-map')]
        self.xwin = 0
        self.ywin = 0

        mapData = _engine.maps[self._currentMapName]
        self.layercount = len(mapData.layers)

        for (i, layer) in enumerate(mapData.layers):
            for entity in layer.entities:
                self.entities[entity.label] = Entity(
                    x=entity.x,
                    y=entity.y,
                    layer=i,
                    spritename=entity.sprite,
                )

    def GetMetaData(self):
        global _engine
        return dict(_engine.maps[self._currentMapName]['information']['meta'])

    def GetZones(self, layerIndex):
        global _engine
        mapData = _engine.maps[self._currentMapName]
        zoneMetadatas = mapData['zones']

        zoneTuples = []
        for zone in mapData['layers'][layerIndex].zones:
            scriptName = None
            for zoneMetadata in zoneMetadatas:
                if zoneMetadata.label == zone.label:
                    scriptName = zoneMetadata.script
                    break

            zoneTuples.append((
                zone['x'],
                zone['y'],
                zone['width'],
                zone['height'],
                scriptName
            ))
        return zoneTuples

    def FindLayerByName(self, name):
        global _engine
        mapData = _engine.maps[self._currentMapName]
        for (i, layer) in enumerate(mapData.layers):
            if layer.label == name:
                return i
        return None

Map = _MapClass()

class Sound(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def Play(self):
        pass # TODO

    def Pause(self):
        pass # TODO
    # TODO other members...

class _VideoClass(object):
    def __init__(self):
        self.xres = None
        self.yres = None
        #colours = None # TODO

    def Blit(self, image, x, y, blendmode=None):
        global _engine
        # Theoretically, we should be discarding the alpha channel of anything
        # that we blit as "opaque", but it's likely that any such graphics
        # already lack an alpha channel.
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        _engine.ctx.drawImage(image._el, x, y)

    def ClearScreen(self):
        global _engine
        _engine.ctx.fillStyle = 'rgb(0, 0, 0)'
        _engine.ctx.fillRect(0, 0, _engine.width, _engine.height)

    def ClipScreen(self, left=None, top=None, right=None, bottom=None):
        global _engine
        # Pop and immediately save pristine state
        _engine.ctx.restore()
        _engine.ctx.save()
        if not all(x is None for x in [left, top, right, bottom]):
            _engine.ctx.rect(left, top, right - left, bottom - top)
            _engine.ctx.clip()

    def DrawPixel(self, x, y, colour, blendmode=None):
        global _engine
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        _engine.ctx.fillStyle = _RGBAToCSS(colour)
        _engine.ctx.fillRect(x, y, 1, 1)

    def DrawRect(self, x1, y1, x2, y2, colour, fill=None, blendmode=None):
        global _engine
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        if fill is True:
            _engine.ctx.fillStyle = _RGBAToCSS(colour)
            # TODO: Maybe check on negative dimension behavior?
            _engine.ctx.fillRect(x1, y1, x2 - x1, y2 - y1)
        else:
            raise NotImplementedError() # TODO

    def GrabImage(self, x1, y1, x2, y2):
        global _engine
        width = x2 - x1
        height = y2 - y1
        canvasEl, ctx = _makeCanvasAndContext(width, height)
        ctx.drawImage(_engine.canvasEl, -x1, -y1)
        return Canvas(width, height, canvasEl, ctx)

    def ScaleBlit(self, image, x, y, width, height, blendmode=None):
        global _engine
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        _engine.ctx.drawImage(image._el, 0, 0, image.width, image.height, x, y, width, height)

    def ShowPage(self):
        global _engine
        _engine.displayCtx.drawImage(_engine.canvasEl, 0, 0)
        # Pretty sure any clipping gets reset here...
        #self.ClipScreen()

    def TintBlit(self, image, x, y, tintColor, blendMode=None):
        # TODO: Honor tint color
        self.Blit(image, x, y, blendMode)

    def TintDistortBlit(self, image, upLeft, upRight, downRight, downLeft, blendmode=None):
        (upLeftX, upLeftY, upLeftTint) = upLeft
        (upRightX, upRightY, upRightTint) = upRight
        (downRightX, downRightY, downRightTint) = downRight
        (downLeftX, downLeftY, downLeftTint) = downLeft
        # TODO: Actually implement.

    # TODO other members...

Video = _VideoClass()

_KeycodeMap = {
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

def _makeCanvasAndContext(width, height):
    el = window.document.createElement('canvas')
    el.width = width
    el.height = height
    ctx = el.getContext('2d')
    ctx.mozImageSmoothingEnabled = False
    ctx.webkitImageSmoothingEnabled = False
    ctx.msImageSmoothingEnabled = False
    ctx.imageSmoothingEnabled = False
    # We maintain one pristine state on the stack for resetting
    # clipping.
    ctx.save()
    return (el, ctx)

class _Engine(object):
    def __init__(self):
        self.canvasEl = None
        self.ctx = None
        self.displayCanvasEl = None
        self.displayCtx = None
        self.height = None
        self.imageEls = {}
        self.startMsec = None
        self.width = None
        self.maps = None
        self.sprites = None

    def getImageEl(self, imagePath):
        return self.imageEls['winter/' + imagePath]

    def run(self, task, mapsPath, spritesPath, imagePaths, systemFontData):
        self.startMsec = window.Date.now()
        self.width = 320
        self.height = 240
        self.systemFontData = systemFontData

        Video.xres = self.width
        Video.yres = self.height

        self.canvasEl, self.ctx = _makeCanvasAndContext(self.width, self.height)
        self.displayCanvasEl, self.displayCtx = _makeCanvasAndContext(self.width, self.height)

        self.displayCanvasEl.style.border = "1px solid"
        window.document.body.appendChild(self.displayCanvasEl)

        promises = []
        for path in imagePaths:
            def loadImage(resolve, reject):
                imageEl = window.Image.new()
                # TODO: Handle image load failure?
                imageEl.addEventListener('load', resolve)
                imageEl.src = path
                self.imageEls[path] = imageEl

                # TODO: Not sure what's going on, but for some reason it seems
                # adding the image element to the page with a non-none display
                # is a prerequisite to having its width and height properties
                # populated, even after waiting for the load event, contrary to
                # all documentation seen online.  Observed in Chrome 59,
                # Firefox 54.
                imageEl.style.position = "absolute"
                imageEl.style.top = "0"
                imageEl.style.left = "0"
                imageEl.style.opacity = "0"
                window.document.body.appendChild(imageEl)
            promises.append(window.Promise.new(loadImage))

        def loadJson(path):
            def fn(resolve, reject):
                xhr = window.XMLHttpRequest.new()
                def onLoad(*args):
                    # TODO: Error handling?
                    json = window.JSON.parse(xhr.responseText)
                    resolve(json)
                xhr.addEventListener('load', onLoad)
                # TODO: Error handling?
                xhr.open('GET', path)
                xhr.send()
            return window.Promise.new(fn)

        def setMapJson(json):
            self.maps = json

        def setSpriteJson(json):
            self.sprites = json

        promises.append(loadJson(mapsPath).then(setMapJson))
        promises.append(loadJson(spritesPath).then(setSpriteJson))

        def onKeyDown(event):
            global _KeycodeMap
            if event.defaultPrevented:
                return
            if event.key not in _KeycodeMap:
                return
            control = Input.keyboard[_KeycodeMap[event.key]]
            control._pressed = 1
            control._position = 1
            event.preventDefault()

        def onKeyUp(event):
            global _KeycodeMap
            if event.defaultPrevented:
                return
            if event.key not in _KeycodeMap:
                return
            control = Input.keyboard[_KeycodeMap[event.key]]
            control._position = 0
            event.preventDefault()

        window.addEventListener('keydown', onKeyDown, True)
        window.addEventListener('keyup', onKeyUp, True)

        def runFrame(timestamp):
            nonlocal task
            try:
                value = next(task)
            except StopIteration:
                print("Engine done.")
                task = None
            else:
                window.requestAnimationFrame(runFrame)

        def startEngine(obj):
            print("Starting engine...")
            window.requestAnimationFrame(runFrame)

        window.Promise.all(promises).then(startEngine)

_engine = None

def Run(task, mapsPath, spritesPath, imagePaths, systemFontData):
    global _engine
    if _engine is not None:
        raise RuntimeError("Already started")
    _engine = _Engine()
    _engine.run(
        task=task,
        mapsPath=mapsPath,
        spritesPath=spritesPath,
        imagePaths=imagePaths,
        systemFontData=systemFontData
    )
