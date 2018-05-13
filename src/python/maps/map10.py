import ika
from soulreaver import SoulReaver
from thing import Thing
from rune import FireRune
import sound

def AutoExec(engineRef):
    if 'fireguard' not in engineRef.saveFlags:
        engineRef.mapThings.append(RuneListener(engineRef))

    if 'firerune' in engineRef.saveFlags:
        ika.Map.RemoveEntity(ika.Map.entities['demiyeti'])
    else:
        engineRef.mapThings.append(DeathListener(engineRef))

def to9(engineRef):
    yield from engineRef.mapSwitchTask('map09.ika-map', (engineRef.player.x, 1 * 16))

class DeathListener(Thing):
    'Waits until the yeti is dead, then drops the fire rune.'
    def __init__(self, engineRef, yeti=None):
        self.engineRef = engineRef
        self.yeti = yeti

    def update(self):
        if not self.yeti:
            # have to get the entity here, since it hasn't been created yet
            # in AutoExec. (if we had more time, I'd fix that problem instead of
            # doing this)
            sound.playMusic("music/Competative.xm")
            self.yeti = self.engineRef.entFromEnt[
                ika.Map.entities['demiyeti'].name
                ]
        elif self.yeti.stats.hp == 0:
            if 'nearend' not in self.engineRef.saveFlags:
                e = ika.Entity(71, 132, 2, 'firerune.ika-sprite')
                e.name = 'firerune'
                self.engineRef.addEntity(
                    FireRune(e)
                    )
            else:
                sound.playMusic("music/winter.ogg")
                self.engineRef.saveFlags['fireguard'] = 'True'

            return True

    def draw(self):
        pass

class RuneListener(object):
    def __init__(self, engineRef):
        self.engineRef = engineRef

    def update(self):
        if 'nearend' in self.engineRef.saveFlags:
            sound.playMusic('music/resurrection.it')
            y = SoulReaver(ika.Entity(21*16, 13*16, 2, 'soulreaver.ika-sprite'))
            self.engineRef.addEntity(y)
            self.engineRef.mapThings.append(DeathListener(self.engineRef, y))
            return True

    def draw(self):
        pass
