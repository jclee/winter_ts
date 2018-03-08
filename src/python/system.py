import ika
import engine
import intro
import sound

import controls
import subscreen

engineObj = None

def mainTask():
    global engineObj
    controls.init()
    subscreen.init()

    c = controls.readConfig('controls.cfg')
    if c is None:
        c = controls.defaultControls
        controls.writeConfig('controls.cfg', c)
    controls.setConfig(c)

    introMusic = ika.Sound('music/Existing.s3m')

    engineObj = engine.Engine()

    # TODO: Reenable
    #yield from intro.introTask()
    #
    #while True:
    #    sound.fader.kill()
    #    introMusic.position = 0
    #    introMusic.Play()
    #    # Workaround for Brython "yield from" expression bugs:
    #    resultRef = [None]
    #    yield from intro.menuTask(resultRef)

    #    if resultRef[0] == 0:
    #        introMusic.Pause()
    #        yield from engineObj.beginNewGameTask()
    #    elif resultRef[0] == 1:
    #        introMusic.Pause()
    #        yield from engineObj.loadGameTask()
    #    elif resultRef[0] == 2:
    #        break
    #    else:
    #        assert False, 'Wacky intro menu result %i! :o' % resultRef[0]
    yield from engineObj.beginNewGameTask()

    ika.Exit()

