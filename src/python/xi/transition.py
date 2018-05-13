import ika

DEFAULT_TIME = 30

class Transition(object):
    def __init__(self):
        self.children = []

    def findChild(self, child):
        for i,iter in enumerate(self.children):
            if iter.theWindow == child:
                return i
        return None

    def hasChild(self, child):
        return self.findChild(child) is not None

    def addChild(self, child, startRect = None, endRect = None, time = None):
        self.removeChild(child)
        r = child.Rect
        self.children.append(WindowMover(child, startRect or r, endRect or r, time or DEFAULT_TIME))

    def removeChild(self, child):
        i = self.findChild(child)
        if i is not None:
            self.children.pop(i)

    def update(self, timeDelta):
        for i, iter in enumerate(self.children):
            iter.update(timeDelta)

            if iter.isDone():
                self.children.pop(i)

    def draw(self):
        for child in self.children:
            child.draw()

    def executeTask(self):
        now = ika.GetTime()
        done = False
        while not done:
            done = True

            yield None
            ika.Map.Render()

            t = ika.GetTime()
            delta = t - now
            now = t
            for child in self.children:
                if not child.isDone():
                    done = False
                    child.update(delta)
                child.draw()

            ika.Video.ShowPage()

class WindowMover(object):
    def __init__(self, theWindow, startRect, endRect, time):
        self.endTime = float(time)
        self.time = 0.0

        # specifying just a position is fine: we'll use the current size of the window to fill in the gap
        if len(startRect) == 2: startRect += theWindow.Size
        if len(endRect) == 2:   endRect += theWindow.Size

        self.theWindow = theWindow
        self.startRect = startRect
        self.endRect = endRect

        # change in position that occurs every tick.
        self.delta = [(e - s) / self.endTime for s, e in zip(startRect, endRect)]

        # Looks like "window" is special for Brython...
        #self.window.Rect = startRect
        self.theWindow.Rect = startRect

    def isDone(self):
        return self.time >= self.endTime

    def update(self, timeDelta):
        if self.time + timeDelta >= self.endTime:
            self.time = self.endTime
            self.theWindow.Rect = self.endRect
        else:
            self.time += timeDelta

            # typical interpolation stuff
            # maybe parameterize the algorithm, so that we can have nonlinear movement.
            # Maybe just use a matrix to express the transform.
            self.theWindow.Rect = [int(d * self.time + s) for s, d in zip(self.startRect, self.delta)]

    def draw(self):
        self.theWindow.draw()
