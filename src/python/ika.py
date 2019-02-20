from browser import window

def DelayTask(time):
    targetEnd = window.Date.now() + (time * 10)
    # Busy waiting, sort of... :(
    while targetEnd > window.Date.now():
        yield None

def Exit():
    print("Exiting.") # TODO

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

class _Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def Entity(x, y, layer, spritename):
    return Map.addEntity(x, y, layer, spritename)

def removeEntity(ent):
    Map.RemoveEntity(ent)

def Font(file_name):
    global _engine
    return window.FontClass.new(_engine)

def GetImage(init_arg):
    global _engine
    return _engine.getImage(init_arg)

class _InputClass(object):
    def __init__(self):
        self.keyboard = _KeyboardClass()

    def getKey(self, key):
        return self.keyboard[key]

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

class Snow(object):
    def __init__(self, count=100, velocity=(0, 0.5), colour=RGB(255, 255, 255)):
        self._time = 0.0
        r, g, b, a = GetRGB(colour)

        self._count = count
        (self._vx, self._vy) = velocity
        self._r = r / 255.0
        self._g = g / 255.0
        self._b = b / 255.0

    def update(self):
        self._time += 10.0

    def draw(self):
        global _engine
        _engine.drawSnow(self._time, self._count, self._vx, self._vy, self._r, self._g, self._b)

_engine = window.Engine.new(Input.getKey)
Map = _engine.map
Video = _engine._video

def hypot(x, y):
    return window.Math.sqrt(x * x + y * y)

def SetLocalStorageItem(key, value):
    window.localStorage.setItem('wintergame/' + key, value)

def GetLocalStorageItem(key):
    return window.localStorage.getItem('wintergame/' + key)

def Run(task):
    global _engine

    def taskFn():
        nonlocal task
        try:
            value = next(task)
        except StopIteration:
            return False
        else:
            return True
    _engine.run(taskFn)
