from browser import window

Opaque = 0
Matte = 1
AlphaBlend = 2
AddBlend = 3
SubtractBlend = 4
MultiplyBlend = 5
PreserveBlend = 6

def Delay(time):
    raise RuntimeError("Use DelayTask instead.")

def DelayTask(time):
    targetEnd = window.Date.now() + (time * 10)
    # Busy waiting... :(
    while targetEnd > window.Date.now():
        yield None

def Exit():
    pass # TODO

def GetCanvasEl():
    global _engine
    return _engine.canvasEl

def GetTime():
    global _engine
    deltaMsec = window.Date.now() - _engine.startMsec
    return (deltaMsec * 10)

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

class Font(object):
    def __init__(self, file_name):
        self._file_name = file_name

    # TODO other members...

class Image(object):
    def __init__(self, init_arg):
        global _engine
        if isinstance(init_arg, str):
            self._path = init_arg
            el = _engine.getImageEl(self._path)
            self.width = el.width
            self.height = el.height
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

    @staticmethod
    def Update():
        pass # TODO

    # TODO other members...

Input = _InputClass()

class _MapClass(object):
    def Render():
        raise NotImplementedError() # TODO

    # TODO other members...

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
    xres = None
    yres = None
    #colours = None # TODO

    @staticmethod
    def Blit(image, x, y, blendmode=None):
        global _engine
        # Theoretically, we should be discarding the alpha channel of anything
        # that we blit as "opaque", but it's likely that any such graphics
        # already lack an alpha channel.
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        imageEl = _engine.getImageEl(image._path)
        _engine.ctx.drawImage(imageEl, x, y)

    @staticmethod
    def ClearScreen():
        global _engine
        _engine.ctx.fillStyle = 'rgb(0, 0, 0)'
        _engine.ctx.fillRect(0, 0, _engine.width, _engine.height)

    @staticmethod
    def DrawPixel(x, y, colour, blendmode=None):
        global _engine
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        _engine.ctx.fillStyle = _RGBAToCSS(colour)
        _engine.ctx.fillRect(x, y, 1, 1)

    @staticmethod
    def DrawRect(x1, y1, x2, y2, colour, fill=None, blendmode=None):
        global _engine
        if blendmode not in [None, Opaque, Matte]:
            raise NotImplementedError() # TODO: Handle more complicated blendmodes.
        if fill is True:
            _engine.ctx.fillStyle = _RGBAToCSS(colour)
            # TODO: Maybe check on negative dimension behavior?
            _engine.ctx.fillRect(x1, y1, x2 - x1, y2 - y1)
        else:
            raise NotImplementedError() # TODO

    @staticmethod
    def ScaleBlit(image, x, y, width, height, blendmode=None):
        raise NotImplementedError() # TODO

    @staticmethod
    def ShowPage():
        global _engine
        _engine.displayCtx.drawImage(_engine.canvasEl, 0, 0)

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

    def getImageEl(self, imagePath):
        return self.imageEls[imagePath]

    def run(self, task, imagePaths):
        self.startMsec = window.Date.now()
        self.width = 320
        self.height = 240

        Video.xres = self.width
        Video.yres = self.height

        def makeCanvasAndContext():
            el = window.document.createElement('canvas')
            el.width = self.width
            el.height = self.height
            ctx = el.getContext('2d')
            ctx.mozImageSmoothingEnabled = False
            ctx.webkitImageSmoothingEnabled = False
            ctx.msImageSmoothingEnabled = False
            ctx.imageSmoothingEnabled = False
            return (el, ctx)

        self.canvasEl, self.ctx = makeCanvasAndContext()
        self.displayCanvasEl, self.displayCtx = makeCanvasAndContext()

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
            promise = window.Promise.new(loadImage)
            promises.append(promise)

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

        def drawFrame(timestamp):
            nonlocal task
            try:
                value = next(task)
            except StopIteration:
                print("Engine done.")
                task = None
            else:
                window.requestAnimationFrame(drawFrame)

        def startEngine(obj):
            print("Starting engine...")
            window.requestAnimationFrame(drawFrame)

        window.Promise.all(promises).then(startEngine)

_engine = None

def Run(task, imagePaths):
    global _engine
    if _engine is not None:
        raise RuntimeError("Already started")
    _engine = _Engine()
    _engine.run(task, imagePaths)
