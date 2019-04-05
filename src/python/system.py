from browser import window
import engine
import ika

def _mainTask(_engine):
    introMusic = ika.Sound('music/Existing.s3m')

    # TODO: clean up... :|
    engineObj = engine.Engine(_engine)

    # TODO: Reenable
    #yield from ika.asTask(window.intro.introTask(engineObj))
    
    while True:
        engineObj.fader.kill()
        introMusic.position = 0
        introMusic.Play()
        # Workaround for Brython "yield from" expression bugs:
        resultRef = [None]
        def setResult(r): resultRef[0] = r
        yield from ika.asTask(window.intro.menuTask(engineObj, setResult))

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

    print("Exiting.") # TODO

def main():
    _engine = window.Engine.new()
    task = _mainTask(_engine)
    def taskFn():
        nonlocal task
        try:
            # TODO: May be able to use yielded generator as a goto.
            value = next(task)
        except StopIteration:
            return False
        else:
            return True
    _engine.run(taskFn)

if __name__ == '__main__':
    main()
