# Stand-in load/save menu code

import controls
import effects
import gui
import ika
from saveload import SaveGame

class SaveGameFrame(gui.Frame):
    def __init__(self, engineRef, icons, save=None):
        gui.Frame.__init__(self, engineRef)
        self.save = save
        self.layout = gui.VerticalBoxLayout()
        self.addChild(self.layout)
        self.update(icons)

    def update(self, icons):
        if self.save:
            stats = self.save.stats
            self.layout.setChildren([
                gui.HorizontalBoxLayout(
                    gui.StaticText(text='HP%03i/%03i' % (stats.hp, stats.maxhp)),
                    gui.Spacer(width=16),
                    gui.StaticText(text='Lv. %02i' % stats.level)
                ),
                gui.FlexGridLayout(4,
                    icons['att'], gui.StaticText(text='%02i  ' % stats.att),
                    icons['mag'], gui.StaticText(text='%02i  ' % stats.mag),
                    icons['pres'], gui.StaticText(text='%02i  ' % stats.pres),
                    icons['mres'], gui.StaticText(text='%02i  ' % stats.mres)
                )
            ])

            self.layout.layout()
            self.autoSize()
        else:
            assert False

class SaveLoadMenu(object):
    def __init__(self, engineRef, saves, saving = False):
        self.icons = dict(
            [(s, gui.Picture(engineRef, img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres')]
        )

        self.cursor = gui.ImageCursor(engineRef, 'gfx/ui/pointer.png')

        self.saves = saves

        boxes = [SaveGameFrame(engineRef, icons=self.icons, save=s) for s in saves]
        if saving:
            boxes.append(gui.TextFrame(engineRef, text='Create New'))
        elif not boxes:
            boxes.append(gui.TextFrame(engineRef, text='No Saves'))

        self.layout = gui.VerticalBoxLayout(pad=16, *boxes)
        self.layout.layout()

        self.cursorPos = 0
        self.oldY = 0 # current offset
        self.curY = 0 # offset we should be at
        if boxes:
            self.wndHeight = self.layout.children[0].getHeight() + 16
        else:
            self.wndHeight = 0 # What should we do here?

        self.layout.setX(16) # doesn't change

    def draw(self):
        self.layout.setY((ika.Video.yres - self.wndHeight) // 2 - self.oldY + 16)
        self.layout.draw()
        self.cursor.draw(16, ika.Video.yres // 2) # cursor doesn't move, everything else does

    def update(self):
        assert len(self.layout.children), 'There should be at least one frame in here. (either indicating no saves, or to create a new save.'

        if self.curY < self.oldY:
            self.oldY -= 2
        elif self.curY > self.oldY:
            self.oldY += 2
        else:
            if controls.up() and self.cursorPos > 0:
                self.cursorPos -= 1
                self.curY = self.cursorPos * self.wndHeight
            elif controls.down() and self.cursorPos < len(self.layout.children) - 1:
                self.cursorPos += 1
                self.curY = self.cursorPos * self.wndHeight
            elif controls.attack():
                return self.cursorPos
            elif controls.cancel():
                return gui.Cancel

            return None

def readSaves(engineRef):
    saves = []

    try:
        i = 0
        while True:
            saves.append(SaveGame(engineRef, 'save%i' % i))
            i += 1
    except IOError:
        return saves

def loadMenuTask(engineRef, resultRef, fadeOut=True):
    title = gui.TextFrame(engineRef, text='Load Game')
    title.setPosition((16, 16))
    saves = readSaves(engineRef)
    m = SaveLoadMenu(engineRef, saves, saving=False)

    def draw():
        ika.Video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from effects.fadeInTask(50, draw=draw)

    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()
        yield None

    if fadeOut:
        yield from effects.fadeOutTask(50, draw=draw)

    draw()
    # Hack to get around brython's lack of support for returning values through
    # "yield from":
    if i is gui.Cancel or i >= len(saves):
        resultRef[0] = None
    else:
        resultRef[0] = saves[i]

def saveMenuTask(engineRef):
    title = gui.TextFrame(engineRef, text='Save Game')
    title.setPosition((16, 16))
    saves = readSaves(engineRef)
    m = SaveLoadMenu(engineRef, saves, saving=True)

    def draw():
        ika.Video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from effects.fadeInTask(50, draw=draw)

    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()
        yield None

    if i is not gui.Cancel:
        s = SaveGame.currentGame(engineRef)
        s.save(engineRef, 'save%i' % i)

    yield from effects.fadeOutTask(50, draw=draw)
