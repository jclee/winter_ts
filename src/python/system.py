import ika
from engine import Engine
from intro import intro, menu
import sound

import controls
controls.init()

import subscreen
subscreen.init()


try:
    c = controls.readConfig('controls.cfg')
except IOError:
    c = controls.defaultControls
    controls.writeConfig('controls.cfg', c)
controls.setConfig(c)


introMusic = ika.Sound('music/Existing.s3m')

intro()

while True:
    sound.fader.kill()
    introMusic.position = 0
    introMusic.Play()
    result = menu()
    engine = Engine()

    if result == 0:
        introMusic.Pause()
        engine.beginNewGame()
    elif result == 1:
        introMusic.Pause()
        engine.loadGame()
    elif result == 2:
        break
    else:
        assert False, 'Wacky intro menu result %i! :o' % result

ika.Exit()