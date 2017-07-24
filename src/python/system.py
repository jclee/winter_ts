import ika
import engine
import intro
import sound

import controls
import subscreen

def mainTask():
    controls.init()
    subscreen.init()

    try:
        c = controls.readConfig('controls.cfg')
    except IOError:
        c = controls.defaultControls
        controls.writeConfig('controls.cfg', c)
    controls.setConfig(c)

    introMusic = ika.Sound('music/Existing.s3m')

    yield from intro.introTask()

    # TODO make work
    #while True:
    #    sound.fader.kill()
    #    introMusic.position = 0
    #    introMusic.Play()
    #    result = intro.menu()
    #    engineObj = engine.Engine()
    #
    #    if result == 0:
    #        introMusic.Pause()
    #        engineObj.beginNewGame()
    #    elif result == 1:
    #        introMusic.Pause()
    #        engineObj.loadGame()
    #    elif result == 2:
    #        break
    #    else:
    #        assert False, 'Wacky intro menu result %i! :o' % result

    ika.Exit()
