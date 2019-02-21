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

class SubScreenWindow(gui.Frame):
    def __init__(self, engineRef):
        super(SubScreenWindow, self).__init__(engineRef)
        self.layout = self.createLayout()
        self.addChild(self.layout)
        self.setBorder(self.wnd.iLeft.width)

    def createLayout(self):
        return gui.VerticalBoxLayout()

    def update(self):
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        self.autoSize()

class StatWindow(SubScreenWindow):
    def __init__(self, engineRef):
        super(StatWindow, self).__init__(engineRef)
        self.engineRef = engineRef

    def createContents(self):
        stats = self.engineRef.player.stats
        return (
            gui.StaticText(text='Level %02i' % stats.level),
            gui.StaticText(text='Exp'), gui.StaticText(text=' %06i/' % stats.exp),
            gui.StaticText(text='  %06i' % stats.next),
            # expbar thingie goes here
            gui.StaticText(text='HP'), gui.StaticText(text=' %03i/%03i' % (stats.hp, stats.maxhp)),
            # hp bar
            gui.StaticText(text='MP'), gui.StaticText(text=' %03i/%03i' % (stats.mp, stats.maxmp))
            # mp bar
            )

class AttribWindow(SubScreenWindow):
    def __init__(self, engineRef):
        super(AttribWindow, self).__init__(engineRef)
        self.engineRef = engineRef
        self.icons = dict(
            [(s, gui.Picture(engineRef, img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres')]
        )

    def createLayout(self):
        return gui.FlexGridLayout(cols=2, pad=0)

    def createContents(self):
        stats = self.engineRef.player.stats
        return (
            self.icons['att'], gui.StaticText(text='...%03i' % stats.att),
            self.icons['mag'], gui.StaticText(text='...%03i' % stats.mag),
            self.icons['pres'], gui.StaticText(text='...%03i' % stats.pres),
            self.icons['mres'], gui.StaticText(text='...%03i' % stats.mres)
            )

class MagicWindow(SubScreenWindow):
    def __init__(self, engineRef):
        SubScreenWindow.__init__(self, engineRef)
        self.engineRef = engineRef

    def createLayout(self):
        return gui.VerticalBoxLayout()

    def createContents(self):
        txt = ['Magic:']
        if 'firerune' in self.engineRef.saveFlags:
            txt.append('Z...Hearth Rend')
        if 'windrune' in self.engineRef.saveFlags:
            txt.append('X...Crushing Gale')
        if 'waterrune' in self.engineRef.saveFlags:
            txt.append('C...Healing Rain')
        if 'cowardrune' in self.engineRef.saveFlags:
            txt.append('B...Shiver')

        return (gui.StaticText(text=txt),)

class MenuWindow(gui.Menu):
    def __init__(self, engineRef):
        gui.Menu.__init__(self, engineRef, textctrl=gui.ScrollableTextFrame(engineRef))
        self.addText([
            'Resume',
            #'Controls',
            #'Load Game',
            'Exit'
        ])
        self.autoSize()
        self.setBorder(self.textCtrl.wnd.iLeft.width)

class PauseScreen(object):
    def __init__(self, engineRef):
        self.statWnd = StatWindow(engineRef)
        self.attribWnd = AttribWindow(engineRef)
        self.magWnd = MagicWindow(engineRef)
        self.menu = MenuWindow(engineRef)

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
            if result is gui.Cancel or result == 0:
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
