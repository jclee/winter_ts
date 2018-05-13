import ika
import engine
import intro

import subscreen

def _mainTask():
    subscreen.init()

    introMusic = ika.Sound('music/Existing.s3m')

    engineObj = engine.Engine()

    # TODO: Reenable
    #yield from intro.introTask()
    
    while True:
        engineObj.fader.kill()
        introMusic.position = 0
        introMusic.Play()
        # Workaround for Brython "yield from" expression bugs:
        resultRef = [None]
        yield from intro.menuTask(resultRef)

        if resultRef[0] == 0:
            introMusic.Pause()
            yield from engineObj.beginNewGameTask()
        elif resultRef[0] == 1:
            introMusic.Pause()
            yield from engineObj.loadGameTask()
        elif resultRef[0] == 2:
            break
        else:
            assert False, 'Wacky intro menu result %i! :o' % resultRef[0]

    ika.Exit()

def main():
    ika.Run(_mainTask())

if __name__ == '__main__':
    main()
