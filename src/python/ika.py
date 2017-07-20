# something

class _KeyboardClass(object):
    pass

    def __getitem__(self, key):
        pass

class _ControlClass(object):
    pass

class _JoystickClass(object):
    def __init__(self):
        self.axes = []
        self.reverseAxes = []
        self.buttons = []

class _InputClass(object):
    def __init__(self):
        self.keyboard = _KeyboardClass()
        self.joysticks = [_JoystickClass()]

    def Update():
        pass

Input = _InputClass()

class Sound(object):
    pass
