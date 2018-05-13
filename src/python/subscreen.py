import ika

from xi.menu import Menu, Cancel
from xi.scrolltext import ScrollableTextFrame
import xi.gui as gui
import xi.layout as layout
from xi.transition import Transition
from xi.window import ImageWindow
from xi.cursor import ImageCursor
import effects

from gameover import GameQuitException

class Window(ImageWindow):
    '''
    Specialized xi window.  The only real differences are that it pulls
    its images from separate image files instead of cutting up a single
    image.
    '''
    def __init__(self, nameTemplate):
        self.iTopleft, self.iTopright, self.iBottomleft, self.iBottomright = [
            ika.Image(nameTemplate % i) for i in
                ('top_left', 'top_right', 'bottom_left', 'bottom_right')]
        self.iLeft, self.iRight, self.iTop, self.iBottom = [
            ika.Image(nameTemplate % i) for i in
                ('left', 'right', 'top', 'bottom')]

        self.iCentre = ika.Image(nameTemplate % 'background')

        self.Blit = ika.Video.ScaleBlit
        self.border = 0

class SubScreenWindow(gui.Frame):
    def __init__(self, *args, **kw):
        super(SubScreenWindow, self).__init__(*args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)
        self.Border = self.wnd.iLeft.width

    def createLayout(self):
        return layout.VerticalBoxLayout()

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
        return layout.FlexGridLayout(cols=2, pad=0)

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
        return layout.VerticalBoxLayout()

    def createContents(self):
        txt = ['Magic:']
        p = self.engineRef.player.stats
        if p.rend:
            txt.append('Z...Hearth Rend')
        if p.gale:
            txt.append('X...Crushing Gale')
        if p.heal:
            txt.append('C...Healing Rain')
        if p.shiver:
            txt.append('B...Shiver')

        return (gui.StaticText(text=txt),)

class MenuWindow(Menu):
    def __init__(self):
        Menu.__init__(self, textctrl=ScrollableTextFrame())
        self.addText(
            'Resume',
            #'Controls',
            #'Load Game',
            'Exit')
        self.autoSize()
        self.Border = self.textCtrl.wnd.iLeft.width

class PauseScreen(object):
    def __init__(self, engineRef):
        assert _initted
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
        t.addChild(self.statWnd, startRect=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, startRect=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, startRect=(-self.magWnd.Right, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, startRect=(ika.Video.xres, self.menu.Top), time=TIME - 5)

        for i in range(TIME):
            t.update(1)
            o = i * 128 // TIME # tint intensity for this frame
            f = i * len(self.images) // TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o), True)
            self.draw()
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

        self.background = self.images[-1]

    def hideTask(self):
        TIME = 40
        t = Transition()
        t.addChild(self.statWnd, endRect=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, endRect=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, endRect=(-self.magWnd.Right, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, endRect=(ika.Video.xres, self.menu.Top), time=TIME - 5)

        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 // TIME # menu opacity for this frame
            f = i * len(self.images) // TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o // 2), True)
            self.draw(o)
            ika.Video.ShowPage()
            yield from ika.Input.UpdateTask()

    def draw(self, opacity = 255):
        gui.default_window.opacity = opacity
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
            yield from ika.Input.UpdateTask()

            result = self.menu.update()
            if result is Cancel or result == 0:
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

_initted = False

def init():
    global _initted
    _initted = True
    gui.init(
        font=ika.Font('system.fnt'),
        wnd=Window('gfx/ui/win_%s.png'),
        csr=ImageCursor('gfx/ui/pointer.png', hotspot=(14, 6))
        )
