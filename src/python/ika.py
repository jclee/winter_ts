from browser import window

def asTask(jsTask):
    while True:
        result = jsTask.next()
        if window.hasProperty(result, 'value'):
            yield result['value']
        if window.hasProperty(result, 'done') and result['done']:
            break

class Sound(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self.position = 0

    def Play(self):
        pass # TODO

    def Pause(self):
        pass # TODO
    # TODO other members...
