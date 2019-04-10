from browser import window
import ika
from serpent import Serpent

# essentially autoExec
def finalBattle(engineRef):
    if 'finalbattle' in engineRef.saveFlags:
        pass
        # make the river passable
    else:
        engineRef.saveFlags['finalbattle'] = 'True'

        p = engineRef.player

        def walkUp():
            p.move(engineRef.dir.Up, 128)
            p.startAnimation('walk')
            for n in range(128):
                yield None

        p.state = walkUp()

        for n in range(128):
            yield from engineRef.tickTask()
            engineRef.draw()
            engineRef.video.ShowPage()
            yield None

        def noOp():
            while True:
                yield None

        p.startAnimation('stand')
        p.state = noOp()

        for n in range(256):
            # teh earthquake
            engineRef.map.xwin += window.random(-4, 5)
            engineRef.map.ywin += window.random(-4, 5)
            yield from engineRef.tickTask()
            engineRef.draw()
            engineRef.video.ShowPage()
            yield None

        s = Serpent(
            engineRef,
            engineRef.map.addSprite(25 * 16, 24 * 16, p.sprite.layer, 'serpent.ika-sprite')
            )
        s.startAnimation('appear')
        engineRef.addEntity(s)

        for n in range(19, 32):
            # close off the way back
            engineRef.map.SetTile(n, 38, p.sprite.layer, 26)
            engineRef.map.SetTile(n, 39, p.sprite.layer, 32)
            engineRef.map.SetObs(n, 38, p.sprite.layer, True)
            yield from engineRef.tickTask()
            engineRef.draw()
            engineRef.video.ShowPage()
            yield None

        p.state = p.defaultState()

        s.state = s.roarState()
        engineRef.synchTime()

def to31(engineRef):
    if False:
        yield None

def to33(engineRef):
    if False:
        yield None
