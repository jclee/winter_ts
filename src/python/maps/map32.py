import ika
import savedata
import dir
from serpent import Serpent

# essentially autoExec
def finalBattle(engineRef):
    if 'finalbattle' in savedata.__dict__:
        pass
        # make the river passable
    else:
        savedata.__dict__['finalbattle'] = 'True'

        p = engineRef.player

        def walkUp():
            p.move(dir.UP, 128)
            p.anim = 'walk'
            for n in range(128):
                yield None

        p.state = walkUp()

        for n in range(128):
            yield from engineRef.tickTask()
            engineRef.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        def noOp():
            while True:
                yield None

        p.anim = 'stand'
        p.state = noOp()

        for n in range(256):
            # teh earthquake
            ika.Map.xwin += ika.Random(-4, 5)
            ika.Map.ywin += ika.Random(-4, 5)
            yield from engineRef.tickTask()
            engineRef.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        s = Serpent(
            engineRef,
            ika.Entity(25 * 16, 24 * 16, p.layer, 'serpent.ika-sprite')
            )
        s.anim = 'appear'
        engineRef.addEntity(s)

        for n in range(19, 32):
            # close off the way back
            ika.Map.SetTile(n, 38, p.layer, 26)
            ika.Map.SetTile(n, 39, p.layer, 32)
            ika.Map.SetObs(n, 38, p.layer, True)
            yield from engineRef.tickTask()
            engineRef.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        p.state = p.defaultState()

        s.state = s.roarState()
        engineRef.synchTime()

def to31(engineRef):
    if False:
        yield None

def to33(engineRef):
    if False:
        yield None
