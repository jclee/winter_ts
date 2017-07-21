# something

Opaque = 0
Matte = 1
AlphaBlend = 2
AddBlend = 3
SubtractBlend = 4
MultiplyBlend = 5
PreserveBlend = 6

def Delay(time):
    pass # TODO

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
        # TODO: Also handle case where first arg is a canvas?
        self._file_name = init_arg
        # TODO: Actually load image
        self.width = 10 # TODO
        self.height = 10 # TODO

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
    xres = 0 # TODO
    yres = 0 # TODO
    #colours = None # TODO

    @staticmethod
    def Blit(image, x, y, blendmode=None):
        pass # TODO

    @staticmethod
    def ClearScreen():
        pass # TODO

    @staticmethod
    def ClearScreen():
        pass # TODO

    @staticmethod
    def DrawRect(x1, y1, x2, y2, colour, fill=None, blendmode=None):
        pass # TODO

    @staticmethod
    def ScaleBlit(image, x, y, width, height, blendmode=None):
        raise NotImplementedError() # TODO

    @staticmethod
    def ShowPage():
        pass # TODO

    # TODO other members...

Video = _VideoClass()
