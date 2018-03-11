import ika

class _PosControl(object):
    def __init__(self, key):
        self._inputKey = ika.Input.keyboard[key]
    def __call__(self):
        return self._inputKey.Position() > 0

class _PressControl(object):
    def __init__(self, key):
        self._inputKey = ika.Input.keyboard[key]
    def __call__(self):
        return self._inputKey.Pressed()

up = _PosControl('UP')
down = _PosControl('DOWN')
left = _PosControl('LEFT')
right = _PosControl('RIGHT')
attack = _PressControl('SPACE')
enter = _PressControl('SPACE')
cancel = _PressControl('ESCAPE')
rend = _PressControl('Z')
gale = _PressControl('X')
heal = _PressControl('C')
shiver = _PressControl('V')
