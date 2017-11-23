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
    return Map.addEntity(x, y, layer, spritename)

def Font(file_name):
    global _engine
    return window.FontClass.new(_engine)

class Canvas(object):
    def __init__(self, width, height, el, ctx):
        self.width = width
        self.height = height
        self._el = el
        self._ctx = ctx

def Image(init_arg):
    global _engine
    if isinstance(init_arg, str):
        return _engine.getImage(init_arg)
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
Video = _engine._video

def hypot(x, y):
    return window.Math.sqrt(x * x + y * y)

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
