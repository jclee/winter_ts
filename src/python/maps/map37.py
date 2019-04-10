from browser import window
import ika

from carnivore import Carnivore

spawned = 0

def AutoExec(engineRef):
    global spawned
    spawned = 0
    engineRef.mapThings.append(window.Snow.new(engineRef, 100, [.4, 1], [255,192,255]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to36(engineRef):
    yield from engineRef.mapSwitchTask('map36.ika-map', (engineRef.player.sprite.x, 1 * 16))

def releaseAnklebiters(engineRef):
    global spawned

    if not 'dynamite3' in engineRef.saveFlags and not spawned:

        indeces = ((6,6), (9,6), (12,6), (4, 8), (14, 8), (2, 10), (6, 10), (12, 10), (16, 10),
                   (4,11), (14, 11))

        for i in indeces:
            engineRef.addEntity(Carnivore(engineRef, self.engineRef.map.addSprite(i[0]*16+8, i[1]*16, 1, "carnivore.ika-sprite")))

        spawned = 1
    if False:
        yield None
