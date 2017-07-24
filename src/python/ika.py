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

def GetTime():
    global _engine
    deltaMsec = window.Date.now() - _engine.startMsec
    return (deltaMsec * 10)

def RGB(r, g, b, a = 255):
    return (
        (int(r) & 0xff)
        | ((int(g) & 0xff) << 8)
        | ((int(b) & 0xff) << 16)
        | ((int(a) & 0xff) << 24)
    )

class _ControlClass(object):
    def __init__(self):
        self._pressed = False
        self._position = 0

    def Pressed(self):
        return self._pressed

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
        self.up = _ControlClass()
        self.down = _ControlClass()
        self.left = _ControlClass()
        self.right = _ControlClass()
        self.enter = _ControlClass()
        self.cancel = _ControlClass()

        self.keyboard = _KeyboardClass()
        self.joysticks = [_JoystickClass()]

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
    def DrawRect(x1, y1, x2, y2, colour, fill=None, blendmode=None):
        pass # TODO

    @staticmethod
    def ScaleBlit(image, x, y, width, height, blendmode=None):
        raise NotImplementedError() # TODO

    @staticmethod
    def ShowPage():
        global _engine
        _engine.displayCtx.drawImage(_engine.canvasEl, 0, 0)

    # TODO other members...

Video = _VideoClass()

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
