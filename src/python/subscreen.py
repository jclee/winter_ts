import effects
import gui
import ika

from gameover import GameQuitException

class Transition(object):
    def __init__(self):
        self.children = []

    def addChild(self, child, startPos = None, endPos = None, time):
        p = child.getPosition()
        self.children.append(WindowMover(child, startPos or p, endPos or p, time))

    def update(self, timeDelta):
        for i, iter in enumerate(self.children):
            iter.update(timeDelta)

            if iter.isDone():
                self.children.pop(i)

    def draw(self):
        for child in self.children:
            child.draw()

class WindowMover(object):
    def __init__(self, theWindow, startPos, endPos, time):
        self.endTime = float(time)
        self.time = 0.0

        self.theWindow = theWindow
        self.startPos = startPos
        self.endPos = endPos

        # change in position that occurs every tick.
        self.delta = [(e - s) / self.endTime for s, e in zip(startPos, endPos)]

        # Looks like "window" is special for Brython...
        #self.window.setPosition(startPos)
        self.theWindow.setPosition(startPos)

    def isDone(self):
        return self.time >= self.endTime

    def update(self, timeDelta):
        if self.time + timeDelta >= self.endTime:
            self.time = self.endTime
            self.theWindow.setPosition(self.endPos)
        else:
            self.time += timeDelta

            # typical interpolation stuff
            # maybe parameterize the algorithm, so that we can have nonlinear movement.
            # Maybe just use a matrix to express the transform.
            self.theWindow.setPosition([int(d * self.time + s) for s, d in zip(self.startPos, self.delta)])

    def draw(self):
        self.theWindow.draw()

class PauseScreen(object):
    def __init__(self, engineRef):
        self.statWnd = gui.StatWindow.new(engineRef)
        self.attribWnd = gui.AttribWindow.new(engineRef)
        self.magWnd = gui.MagicWindow.new(engineRef)
        self.menu = gui.MenuWindow.new(engineRef)

    def update(self):
        self.statWnd.update()
        self.attribWnd.update()
        self.magWnd.update()
        self.statWnd.dockTop().dockLeft()
        self.attribWnd.setPosition((self.statWnd.getX(), self.statWnd.getBottom() + self.statWnd.getBorder() * 2)) # eek
        self.magWnd.setPosition((self.statWnd.getX(), self.attribWnd.getBottom() + self.attribWnd.getBorder() * 2))
        self.menu.dockRight().dockTop()

    def showTask(self):
        # assume the backbuffer is already filled
        self.images = effects.createBlurImages()
        TIME = 40

        self.update()

        t = Transition()
        t.addChild(self.statWnd, startPos=(-self.statWnd.getRight(), self.statWnd.getY()), time=TIME - 5)
        t.addChild(self.attribWnd, startPos=(-self.attribWnd.getRight(), self.attribWnd.getY()), time=TIME - 5)
        t.addChild(self.magWnd, startPos=(-self.magWnd.getRight(), self.magWnd.getY()), time=TIME - 5)
        t.addChild(self.menu, startPos=(ika.Video.xres, self.menu.getY()), time=TIME - 5)

        startTime = ika.GetTime()
        now = startTime
        endTime = now + TIME
        prevTime = 0
        while now < endTime:
            time = int(now - startTime)
            deltaTime = time - prevTime
            prevTime = time
            if deltaTime > 0:
                t.update(deltaTime)
                o = time * 128 // TIME # tint intensity for this frame
                f = time * len(self.images) // TIME # blur image to draw

                ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o))
                self.draw()
                ika.Video.ShowPage()
            yield None
            now = ika.GetTime()

        # TODO: Not used, but maybe should be?:
        self.background = self.images[-1]

    def hideTask(self):
        TIME = 40
        t = Transition()
        t.addChild(self.statWnd, endPos=(-self.statWnd.getRight(), self.statWnd.getY()), time=TIME - 5)
        t.addChild(self.attribWnd, endPos=(-self.attribWnd.getRight(), self.attribWnd.getY()), time=TIME - 5)
        t.addChild(self.magWnd, endPos=(-self.magWnd.getRight(), self.magWnd.getY()), time=TIME - 5)
        t.addChild(self.menu, endPos=(ika.Video.xres, self.menu.getY()), time=TIME - 5)

        startTime = ika.GetTime()
        now = startTime
        endTime = now + TIME
        prevTime = 0
        while now < endTime:
            time = int(now - startTime)
            deltaTime = time - prevTime
            prevTime = time
            if deltaTime > 0:
                t.update(deltaTime)
                o = (TIME - time) * 255 // TIME # menu opacity for this frame
                f = int((TIME - time) * len(self.images) // TIME) # blur image to draw

                ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o // 2))
                self.draw()
                ika.Video.ShowPage()
            yield None
            now = ika.GetTime()

        self.background = None
        effects.freeBlurImages(self.images)

    def draw(self):
        self.statWnd.draw()
        self.attribWnd.draw()
        self.magWnd.draw()
        self.menu.draw()

    def runTask(self):
        yield from self.showTask()
        while True:
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128))
            self.draw()
            ika.Video.ShowPage()
            yield None

            result = self.menu.update()
            if result == 'cancel' or result == 0:
                break
            elif result is not None:
                if result == 0:
                    raise RuntimeError() # should never happen
                elif result == 1:
                    yield from self.exitGameTask()

        yield from self.hideTask()

    def exitGameTask(self):
        # TODO: shiny fade out
        raise GameQuitException()
