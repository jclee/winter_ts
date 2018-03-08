import ika
import savedata
import system
import dir
from serpent import Serpent

savedata = savedata.__dict__ # fuckit

# essentially autoExec
def finalBattle():
    if 'finalbattle' in savedata:
        pass
        # make the river passable
    else:
        savedata['finalbattle'] = 'True'

        p = system.engineObj.player

        def walkUp():
            p.move(dir.UP, 128)
            p.anim = 'walk'
            for n in range(128):
                yield None

        p.state = walkUp()

        for n in range(128):
            yield from system.engineObj.tickTask()
            system.engineObj.draw()
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
            yield from system.engineObj.tickTask()
            system.engineObj.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        s = Serpent(
            ika.Entity(25 * 16, 24 * 16, p.layer, 'serpent.ika-sprite')
            )
        s.anim = 'appear'
        system.engineObj.addEntity(s)

        for n in range(19, 32):
            # close off the way back
            ika.Map.SetTile(n, 38, p.layer, 26)
            ika.Map.SetTile(n, 39, p.layer, 32)
            ika.Map.SetObs(n, 38, p.layer, True)
            yield from system.engineObj.tickTask()
            system.engineObj.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        p.state = p.defaultState()

        s.state = s.roarState()
        system.engineObj.synchTime()

def to31():
    if False:
        yield None

def to33():
    if False:
        yield None
