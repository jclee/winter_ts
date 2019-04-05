from browser import window

def asTask(jsTask):
    while True:
        result = jsTask.next()
        if window.hasProperty(result, 'value'):
            yield result['value']
        if window.hasProperty(result, 'done') and result['done']:
            break

def DelayTask(time):
    targetEnd = window.Date.now() + (time * 10)
    # Busy waiting, sort of... :(
    while targetEnd > window.Date.now():
        yield None

def Random(low, high):
    return window.Math.floor(window.Math.random() * (high - low)) + low

def Entity(x, y, layer, spritename):
    return Map.addEntity(x, y, layer, spritename)

def removeEntity(ent):
    Map.RemoveEntity(ent)

def GetImage(init_arg):
    global _engine
    return _engine.getImage(init_arg)

class Sound(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self.position = 0

    def Play(self):
        pass # TODO

    def Pause(self):
        pass # TODO
    # TODO other members...

_engine = window.Engine.new()
Map = _engine.map
Controls = _engine.controls
Video = _engine.video

def getEngine():
    global _engine
    return _engine

def hypot(x, y):
    return window.Math.sqrt(x * x + y * y)

def Run(task):
    global _engine

    def taskFn():
        nonlocal task
        try:
            # TODO: May be able to use yielded generator as a goto.
            value = next(task)
        except StopIteration:
            return False
        else:
            return True
    _engine.run(taskFn)
