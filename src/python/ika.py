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

def Random(low, high):
    return window.Math.floor(window.Math.random() * (high - low)) + low

def RGB(r, g, b, a = 255):
    return window.RGB(r, g, b, a)

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

def Entity(x, y, layer, spritename):
    return Map.AddEntity(x, y, layer, spritename)

def Font(file_name):
    global _engine
    return window.FontClass.new(_engine)

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

    def getKey(self, key):
        return self.keyboard[key]

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

class Sound(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self.position = 0

    def Play(self):
        pass # TODO

    def Pause(self):
        pass # TODO
    # TODO other members...

class _VideoClass(object):
    def __init__(self):
        # Resolution used in this game...
        self.xres = 320
        self.yres = 240
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

_engine = window.Engine.new(Input.getKey)
Map = _engine.map

def Run(task, mapsPath, spritesPath, imagePaths, systemFontData):
    global _engine

    def taskFn():
        nonlocal task
        try:
            value = next(task)
        except StopIteration:
            return False
        else:
            return True
    _engine.run(taskFn, mapsPath, spritesPath, imagePaths, systemFontData)
