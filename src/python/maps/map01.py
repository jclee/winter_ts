import ika

from yeti import Yeti
import snow


def AutoExec(engineRef):
    engineRef.mapThings.append(snow.Snow(velocity=(0, 0.5)))
    if 'cowardrune' not in engineRef.saveFlags:
        engineRef.mapThings.append(RuneListener(engineRef))

def to2(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 38 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map02.ika-map', (48 * 16, y))

def to49(engineRef):
    yield from engineRef.mapSwitchTask('map49.ika-map', (14 * 16, 23 * 16))

class RuneListener(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        if 'waterguard' in self.engineRef.saveFlags and 'fireguard' in self.engineRef.saveFlags and 'windguard' in self.engineRef.saveFlags:
            self.engineRef.addEntity(
                Yeti(self.engineRef, ika.Entity(35 * 16, 19 * 16, self.engineRef.player.layer, 'yeti.ika-sprite')))
            return True

    def draw(self):
        pass
