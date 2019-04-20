from browser import window
import ika
import sound
from thing import Thing

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 8000, [-.2, 3]))
    if 'waterrune' not in engineRef.saveFlags:
        engineRef.mapThings.append(RuneListener(engineRef))
    if 'nearend' in engineRef.saveFlags:
        engineRef.mapThings.append(RuneListener(engineRef))

def to3(engineRef):
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map03.ika-map', (x, 1 * 16))

def to5(engineRef):
    yield from engineRef.mapSwitchTask('map05.ika-map', (10 * 16, 19 * 16))

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the fire rune.'
    def __init__(self, engineRef, yeti=None):
        self.engineRef = engineRef
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            self.engineRef.playMusic("music/winter.ogg")
            self.engineRef.saveFlags['waterguard'] = 'True'
            return True

    def draw(self):
        pass

class RuneListener(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        if 'nearend' in self.engineRef.saveFlags and 'waterguard' not in self.engineRef.saveFlags:
            sound.playMusic("music/resurrection.it")
            y = window.yeti.SoulReaver.new(self.engineRef, self.engineRef.map.addSprite(15* 16, 17 * 16, self.engineRef.player.sprite.layer, 'soulreaver.ika-sprite'))
            self.engineRef.addEntity(y)
            self.engineRef.mapThings.append(DeathListener(self.engineRef, y))
            return True
        elif 'waterrune' in self.engineRef.saveFlags and 'nearend' not in self.engineRef.saveFlags:
            self.engineRef.addEntity(
                window.yeti.Yeti.new(self.engineRef, self.engineRef.map.addSprite(15* 16, 32 * 16, self.engineRef.player.sprite.layer, 'yeti.ika-sprite'))
            )
            return True

    def draw(self):
        pass
