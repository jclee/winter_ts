
import ika

import xi.gui as gui
import xi.scrolltext as scrolltext
#import xi.cursor

import xi.sound as sound
import controls

# unique object returned when the user cancels a menu.
# this object's identity is its only attribute, like None.
Cancel = object()

class Menu(gui.Widget):
    '''
    A menu.  A list of textual options displayed in some sort of text container,
    with a cursor that responds to user input, allowing the user to select an option.

    I'll readily admit that this is somewhat limiting.  Doing a SoM style ring menu with
    this class is not very realistic, but it could be implemented as its own class. (and
    probably should, considering how different it is from this.
    '''
    def __init__(self, *args, **kwargs):
        gui.Widget.__init__(self, *args)
        #self.textCtrl = kwargs.get('textctrl') or scrolltext.ScrollableTextFrame()
        self.textCtrl = kwargs.get('textctrl') or scrolltext.ScrollableTextLabel()
        self.cursor = kwargs.get('cursor') or gui.default_cursor
        self.cursorY = 0
        self.cursorPos = 0
        self.cursorSpeed = 2 # speed at which the cursor moves (in pixels per update)
        self.addChild(self.textCtrl)

    def setCursorPos(self, value):
        value = max(0, value)
        self.cursorPos = min(len(self.Text), value)

    def setWidth(self, value):
        self.width = value
        self.textCtrl.Width = value - self.cursor.Width

    def setHeight(self, value): self.height = self.textCtrl.Height = value
    def setSize(self, value):   self.Width, self.Height = value
    def setText(self, value):   self.textCtrl.Text = value
    def setBorder(self, value): self.textCtrl.Border = value

    Width = property(lambda self: self.width, setWidth)
    Height = property(lambda self: self.height, setHeight)
    Size = property(lambda self: (self.width, self.height), setSize)
    CursorY = property(lambda self: self.cursorY)
    CursorPos = property(lambda self: self.cursorPos, setCursorPos)
    Font = property(lambda self: self.textCtrl.Font)
    Text = property(lambda self: self.textCtrl.Text, setText)
    Border = property(lambda self: self.textCtrl.Border, setBorder)

    def addText(self, *args):
        self.textCtrl.addText(*args)

    def autoSize(self):
        w = self.cursor.Width
        self.textCtrl.Position = (w, 0)
        self.textCtrl.autoSize()
        self.Size = (self.textCtrl.Width + w, self.textCtrl.Height)

    def update(self):
        '''
        Performs one tick of menu input.  This includes scrolling things around, and updating
        the position of the cursor, based on user interaction.

        If the user has selected an option, then the return value is the index of that option.
        If the user hit the cancel (ESC) key, the Cancel object is returned.
        else, None is returned, to signify that nothing has happened yet.
        '''
        # Presumably callers are already updating input...
        #yield from ika.Input.UpdateTask()
        cy = self.cursorY
        unpress = False # lame unpress faking
        # TODO: handle it the manly way, by making the cursor repeat after a moment

        # update the cursor
        ymax = max(0, len(self.Text) * self.Font.height - self.textCtrl.Height)
        assert 0 <= self.cursorPos <= len(self.Text), 'cursorPos out of range 0 <= %i <= %i' % (self.cursorPos, len(self.Text))

        delta = self.cursorPos * self.Font.height - self.textCtrl.YWin - cy
        if delta > 0:
            if cy < self.textCtrl.Height - self.Font.height:
                self.cursorY += self.cursorSpeed
            else:
                self.textCtrl.YWin += self.cursorSpeed
        elif delta < 0:
            if cy > 0:
                self.cursorY -= self.cursorSpeed
            elif self.textCtrl.YWin > 0:
                self.textCtrl.YWin -= self.cursorSpeed
        else:
            # Maybe this isn't a good idea.  Maybe it is.
            # only move the cursor if delta is zero
            # that way movement doesn't get bogged
            # down by a cursor that moves too slowly
            if controls.up() and self.cursorPos > 0:
                if not unpress:
                    self.cursorPos -= 1
                    sound.cursormove.Play()
                    unpress = True
            elif controls.down() and self.cursorPos < len(self.Text) - 1:
                if not unpress:
                    self.cursorPos += 1
                    sound.cursormove.Play()
                    unpress = True
            elif controls.enter():
                return self.cursorPos
            elif controls.cancel():
                return Cancel
            else:
                unpress = False
                return None

    def draw(self, xoffset = 0, yoffset = 0):
        self.textCtrl.draw(self.x + xoffset, self.y + yoffset)
        self.cursor.draw(
            self.x + self.textCtrl.x + xoffset,
            self.y + self.textCtrl.y + yoffset + self.cursorY + (self.Font.height // 2)
            )
