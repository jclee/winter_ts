import effects
import gui
import ika

from gameover import GameQuitException

DEFAULT_TIME = 30

class Transition(object):
    def __init__(self):
        self.children = []

    def addChild(self, child, startPos = None, endPos = None, time = None):
        p = child.Position
        self.children.append(WindowMover(child, startPos or p, endPos or p, time or DEFAULT_TIME))

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
    def __init__(self, theWindow, startPos, endPos, time):
        self.endTime = float(time)
        self.time = 0.0

        self.theWindow = theWindow
        self.startPos = startPos
        self.endPos = endPos

        # change in position that occurs every tick.
        self.delta = [(e - s) / self.endTime for s, e in zip(startPos, endPos)]

        # Looks like "window" is special for Brython...
        #self.window.Position = startPos
        self.theWindow.Position = startPos

    def isDone(self):
        return self.time >= self.endTime

    def update(self, timeDelta):
        if self.time + timeDelta >= self.endTime:
            self.time = self.endTime
            self.theWindow.Position = self.endPos
        else:
            self.time += timeDelta

            # typical interpolation stuff
            # maybe parameterize the algorithm, so that we can have nonlinear movement.
            # Maybe just use a matrix to express the transform.
            self.theWindow.Position = [int(d * self.time + s) for s, d in zip(self.startPos, self.delta)]

    def draw(self):
        self.theWindow.draw()

class SubScreenWindow(gui.Frame):
    def __init__(self, *args, **kw):
        super(SubScreenWindow, self).__init__(*args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)
        self.Border = self.wnd.iLeft.width

    def createLayout(self):
        return gui.VerticalBoxLayout()

    def update(self):
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        self.autoSize()

class StatWindow(SubScreenWindow):
    def __init__(self, engineRef, *args, **kw):
        super(StatWindow, self).__init__(*args, **kw)
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
        super(AttribWindow, self).__init__()
        self.engineRef = engineRef
        self.icons = dict(
            [(s, gui.Picture(img='gfx/ui/icon_%s.png' % s))
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
        SubScreenWindow.__init__(self)
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
    def __init__(self):
        gui.Menu.__init__(self, textctrl=gui.ScrollableTextFrame())
        self.addText([
            'Resume',
            #'Controls',
            #'Load Game',
            'Exit'
        ])
        self.autoSize()
        self.Border = self.textCtrl.wnd.iLeft.width

class PauseScreen(object):
    def __init__(self, engineRef):
        self.statWnd = StatWindow(engineRef)
        self.attribWnd = AttribWindow(engineRef)
        self.magWnd = MagicWindow(engineRef)
        self.menu = MenuWindow()

    def update(self):
        self.statWnd.update()
        self.attribWnd.update()
        self.magWnd.update()
        self.statWnd.dockTop().dockLeft()
        self.attribWnd.Position = (self.statWnd.Left, self.statWnd.Bottom + self.statWnd.Border * 2) # eek
        self.magWnd.Position = (self.statWnd.Left, self.attribWnd.Bottom + self.attribWnd.Border * 2)
        self.menu.dockRight().dockTop()

    def showTask(self):
        # assume the backbuffer is already filled
        self.images = effects.createBlurImages()
        TIME = 40

        self.update()

        t = Transition()
        t.addChild(self.statWnd, startPos=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, startPos=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, startPos=(-self.magWnd.Right, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, startPos=(ika.Video.xres, self.menu.Top), time=TIME - 5)

        for i in range(TIME):
            t.update(1)
            o = i * 128 // TIME # tint intensity for this frame
            f = i * len(self.images) // TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o), True)
            self.draw()
            ika.Video.ShowPage()
            yield None

        self.background = self.images[-1]

    def hideTask(self):
        TIME = 40
        t = Transition()
        t.addChild(self.statWnd, endPos=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, endPos=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, endPos=(-self.magWnd.Right, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, endPos=(ika.Video.xres, self.menu.Top), time=TIME - 5)

        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 // TIME # menu opacity for this frame
            f = i * len(self.images) // TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o // 2), True)
            self.draw()
            ika.Video.ShowPage()
            yield None

    def draw(self):
        self.statWnd.draw()
        self.attribWnd.draw()
        self.magWnd.draw()
        self.menu.draw()

    def runTask(self):
        yield from self.showTask()
        while True:
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
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
