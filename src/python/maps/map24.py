import ika

from rune import CowardRune

def AutoExec(engineRef):
    if 'waterguard' in self.engineRef.saveFlags and 'windguard' in self.engineRef.saveFlags and 'fireguard' in self.engineRef.saveFlags:
        engineRef.mapThings.append(AddRune(engineRef))

def to23(engineRef):
    yield from engineRef.mapSwitchTask('map23.ika-map', (5 * 16, 5 * 16))

def to50(engineRef):
    yield from engineRef.mapSwitchTask('map50.ika-map', (9 * 16, 13 * 16))

class AddRune(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        e = self.engineRef.map.addEntity(315, 320, 1, 'cowardrune.ika-sprite')
        e.name = 'cowardrune'
        self.engineRef.addEntity(CowardRune(e))
        return True

    def draw(self):
        pass

