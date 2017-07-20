
import ika
import xi.gui as gui

class ScrollableTextLabel(gui.StaticText):
    '''
    A text label that can potentially hold more text than it can visually display, given
    whatever size it may be at the time.

    The text label's scroll position (YWin) is in pixel coordinates, and can range from 0 to
    its YMax value.
    '''

    def __init__(self, *args):
        gui.StaticText.__init__(self, *args)
        self.ywin = 0
        self.ymax = 0

    def setYWin(self, value):
        self.ywin = min(self.ymax - self.height, value)
        if self.ywin < 0:
            self.ywin = 0

    def setText(self, value):
        self.text = value[:]
        self.ymax = len(self.text) * self.font.height

    YWin = property(lambda self: self.ywin, setYWin)
    YMax = property(lambda self: self.ymax - self.height)
    Text = property(lambda self: self.text, setText)

    def addText(self, *args):
        gui.StaticText.addText(self, *args)
        self.ymax = len(self.text) * self.font.height

    def draw(self, xoffset = 0, yoffset = 0):
        x = self.x + xoffset
        y = self.y + yoffset
        ika.Video.ClipScreen(x, y, x + self.width, y + self.height)

        firstLine = self.ywin / self.font.height
        lastLine = (self.height + self.ywin) / self.font.height + 1

        curY = y - self.ywin % self.font.height
        for line in self.text[firstLine:lastLine]:
            self.font.Print(x, curY, line)
            curY += self.font.height

        ika.Video.ClipScreen()

class ScrollableTextFrame(gui.Frame):
    '''
    Simple combination of ScrollableTextLabel and Frame
    Most of the work here is making the class behave both like a ScrollableTextLabel and
    a Frame at the same time.
    '''

    def __init__(self, *args, **kwargs):
        gui.Frame.__init__(self, *args, **kwargs)

        self.text = ScrollableTextLabel()
        self.addChild(self.text)

    def setYWin(self, value):   self.text.YWin = value
    def setText(self, value):   self.text.Text = value
    def setFont(self, value):   self.text.Font = value

    YWin = property(lambda self: self.text.YWin, setYWin)
    YMax = property(lambda self: self.text.YMax)
    Text = property(lambda self: self.text.Text, setText)
    Font = property(lambda self: self.text.Font, setFont)

    def addText(self, *args):
        self.text.addText(*args)

    def autoSize(self):
        self.text.autoSize()
        self.Size = self.text.Size
