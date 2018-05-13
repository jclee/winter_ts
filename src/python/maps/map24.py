import ika
import savedata

from rune import CowardRune

def AutoExec(engineRef):
    if 'waterguard' in savedata.__dict__ and 'windguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__:
        engineRef.mapThings.append(AddRune())

def to23(engineRef):
    yield from engineRef.mapSwitchTask('map23.ika-map', (5 * 16, 5 * 16))

def to50(engineRef):
    yield from engineRef.mapSwitchTask('map50.ika-map', (9 * 16, 13 * 16))

class AddRune(object):
    def update(self):
        e = ika.Entity(315, 320, 1, 'cowardrune.ika-sprite')
        e.name = 'cowardrune'
        engineRef.addEntity(CowardRune(e))
        return True

    def draw(self):
        pass

