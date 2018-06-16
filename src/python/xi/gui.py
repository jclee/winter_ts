# Basic GUI elements
# coded by Andy Friesen
# copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.

import ika
import controls

default_font = None
default_cursor = None
default_window = None

def init(font, wnd, csr):
    '''
    Initializes defaults for the GUI system.  This MUST be called before
    creating any instances.
    '''
    global default_font, default_window, default_cursor

    default_font = font
    default_window = wnd
    default_cursor = csr

class ImageCursor(object):
    def __init__(self, filename, hotspot = None):
        img = ika.Image(filename)
        self.img = img
        self.hotspot = hotspot or (img.width, img.height // 2)

    def setHotSpot(self, p):
        (x, y) = p
        self.hotspot = int(x), int(y)

    Width = property(lambda self: self.img.width)
    Height = property(lambda self: self.img.height)
    Size = property(lambda self: (self.Width, self.Height))
    HotSpot = property(lambda self: self.hotspot, setHotSpot)

    def draw(self, x, y):
        ika.Video.Blit(self.img, x - self.hotspot[0], y - self.hotspot[1])

class Widget(object):
    '''
    Basic GUI element class.  By itself, the Widget is an invisible container.
    While this may be useful in and of itself, widgets probably won't see much
    direct use.  Subclasses are where the action usually is.
    '''

    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        self.border = 0

    def setX(self, value):      self.x = value
    def setY(self, value):
        self.y = value

    def setWidth(self, value):
        assert value > 0, 'Width must be positive!! (%i)' % value
        self.width = value

    def setHeight(self, value):
        assert value > 0, 'Height must be positive!!! (%i)' % value
        self.height = value

    def setRight(self, value):
        self.x = value - self.width

    def setBottom(self, value):
        self.y = value - self.height

    def setSize(self, value):
        self.Width, self.Height = value

    def setPosition(self, value):
        self.X, self.Y = value

    def setRect(self, rect):
        (x, y, width, height) = rect
        self.Position = (x, y)
        self.Size = (width, height)

    def setBorder(self, value):
        self.border = value

    def stretchHorizontally(self, x1, x2):
        assert x1 < x2, 'x1 (%i) must be smaller than x2! (%i)' % (x1, x2)
        self.Left = x1
        self.Width = x2 - x1

    def stretchVertically(self, y1, y2):
        assert y1 < y2, 'y1 (%i) must be smaller than y2! (%i)' % (y1, y2)
        self.Top = y1
        self.Height = y2 - y1

    def dockTop(self):
        self.Top = self.Border
        return self

    def dockBottom(self):
        self.Bottom = ika.Video.yres - self.Border
        return self

    def dockLeft(self):
        self.Left = self.Border
        return self

    def dockRight(self):
        self.Right = ika.Video.xres - self.Border
        return self

    X = property(lambda self: self.x, setX, doc='Gets or sets the x coordinate of the left edge of the widget')
    Y = property(lambda self: self.y, setY, doc='Gets or sets the y coordinate of the top edge of the widget')
    Left = X
    Top = Y
    Bottom = property(lambda self: self.y + self.height, setBottom, doc='Gets or sets the y coordinate of the bottom edge of the widget.  Setting this does not resize the widget in any case.')
    Right = property(lambda self: self.y + self.height, setRight, doc='Gets or sets the x coordinate of the right edge of th widget.  Setting this does not resize the widget in any case.')
    Width = property(lambda self: self.width, setWidth, doc='Gets or sets the width of the widget')
    Height = property(lambda self: self.height, setHeight, doc='Gets or sets the height of the widget')
    Position = property(lambda self: (self.x, self.y), setPosition, doc='Gets or sets the position of the upper left corner of the widget.  Position is a tuple, ie (x,y)')
    Size = property(lambda self: (self.width, self.height), setSize, doc='Gets or sets the size of the widget.  Size is a tuple.  ie (width, height)')
    Rect = property(lambda self: self.Position + self.Size, setRect, doc='Gets or sets the window rect of the widget.  ie (x, y, width, height)')
    Border = property(lambda self: self.border, setBorder, doc='Gets or sets the size of the border around the widget.')

    def draw(self, xofs = 0, yofs = 0):
        '''
        Draws the widget onscreen.  xofs and yofs are added to the widget's own positional coordinates.
        xofs and yofs are customarily the absolute x/y position of the containing widget, if any.
        '''
        for child in self.children:
            child.draw(xofs + self.x, yofs + self.y)

    def addChild(self, child):
        'Adds a child to the widget.'

        assert child not in self.children, 'Object %o is already a child!'
        self.children.append(child)

    def removeChild(self, child):
        'Removes a child from the widget.'
        assert child in self.children, 'Attempt to remove nonexistent child!'
        self.children.remove(child)

    def hasChild(self, child):
        'Returns True if the widget is a child'
        return child in self.children

    def autoSize(self):
        '''
        Sets the size of the frame such that every child will be visibly contained within it.
        '''
        self.Size = (1, 1)
        for child in self.children:
            self.width = max(self.width, child.Width + child.X)
            self.height = max(self.height, child.Height + child.Y)

class Frame(Widget):
    '''
    A widget that appears as a graphical frame of some sort.
    Frames are most commonly used as container widgets.
    '''
    def __init__(self, x = 0, y = 0, width = 0, height = 0, **kwargs):
        Widget.__init__(self, x, y, width, height)

        self.wnd = kwargs.get('wnd', default_window)
        self.Border = int(self.wnd.Left * 2.0)

    def draw(self, xofs = 0, yofs = 0):
        self.wnd.draw(self.x + xofs, self.y + yofs, self.width, self.height)
        Widget.draw(self, xofs, yofs)

class StaticText(Widget):
    '''
    A widget that appears as some lines of text.
    No frame is drawn.
    '''
    def __init__(self, x = 0, y = 0, w = 0, h = 0, *args, **kwargs):
        Widget.__init__(self, x, y, w, h)

        if 'text' in kwargs:
            if isinstance(kwargs['text'], str):
                self.text = [kwargs['text']]
            else:
                self.text = kwargs['text'][:]
        else:
            self.text = list(args)

        self.font = kwargs.get('font', default_font)

        self.autoSize()

    def setText(self, value):
        self.text = value[:]

    def setFont(self, value):
        self.font = value

    Text = property(lambda self: self.text, setText, doc='Gets or sets the text that is to be displayed.')
    Font = property(lambda self: self.font, setFont, doc='Gets or sets the font used to display the text.')

    def addText(self, *args):
        'Appends text to what is already stored'
        a = [str(i) for i in args]
        self.text.extend(a)

    def clear(self):
        'Clears all the text.'
        self.text = []

    def autoSize(self):
        'Sets the size of the StaticText control such that there is enough room for all the text contained.'
        if self.text:
            self.height = len(self.text) * self.font.height
            self.width = max(
                [ self.font.StringWidth(t) for t in self.text ]
                )
        else:
            self.Size = 1, 1

    def draw(self, xoffset = 0, yoffset = 0):
        y = self.y + yoffset
        x = self.x + xoffset
        for t in self.text:
            self.font.Print(x, y, t)
            y += self.font.height

        Widget.draw(self, xoffset, yoffset)

class TextFrame(Frame):
    '''
    A frame with text in it.  This is a simple convenience class, combining the
    Frame and StaticText controls into a single convenient object.
    '''
    def __init__(self, x = 0, y = 0, width = 0, height = 0, *args, **kwargs):
        Frame.__init__(self, x, y, width, height, *args, **kwargs)

        # way cool.  since keyword arguments are passed on, the font will be set properly.
        # additionally, text will be added just like StaticText.  Consistency totally rules.
        self.text = StaticText(0, 0, width, height, *args, **kwargs)

        self.addChild(self.text)
        self.autoSize()

    def setFont(self, font):
        self.text.Font = font

    Text = property(lambda self: self.text.Text, lambda self, value: self.text.setText(value),
        doc='Gets or sets the text contained by the control.')

    Font = property(lambda self: self.text.Font, setFont,
        doc='Gets or sets the font used for the text contained by the control.')

    def addText(self, *args):
        'Appends text to what is already contained.'

        self.text.addText(*args)

    def autoSize(self):
        'Autosizes the frame such that it is just large enough to contain its text.'
        self.text.autoSize()
        self.Size = self.text.Size

class Picture(Widget):
    '''
    A widget that takes the shape of an image.
    Little else to say.
    '''
    def __init__(self, x = 0, y = 0, width = 0, height = 0, **kwargs):
        Widget.__init__(self, x, y, width, height)
        assert 'img' in kwargs, 'Must specify an img argument to Picture constructor.'
        self.img = kwargs['img']
        if isinstance(self.img, str):
            self.img = ika.Image(self.img)

        self.Size = (width or self.img.width), (height or self.img.height)

        self.drawImage = Picture.drawImage

    def drawImage(img, x, y, width, height):
        '''
        Does the actual drawing.
        The cool part of this is that you can assign a new drawImage method
        to a Picture object to override how it does the drawing.
        '''
        ika.Video.ScaleBlit(img, x, y, width, height)

    drawImage = staticmethod(drawImage)

    def draw(self, xoffset = 0, yoffset = 0):
        self.drawImage(self.img, self.x + xoffset, self.y + yoffset, self.width, self.height)

class ScrollableTextLabel(StaticText):
    '''
    A text label that can potentially hold more text than it can visually display, given
    whatever size it may be at the time.

    The text label's scroll position (YWin) is in pixel coordinates, and can range from 0 to
    its YMax value.
    '''

    def __init__(self, *args):
        StaticText.__init__(self, *args)
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
        StaticText.addText(self, *args)
        self.ymax = len(self.text) * self.font.height

    def draw(self, xoffset = 0, yoffset = 0):
        x = self.x + xoffset
        y = self.y + yoffset
        ika.Video.ClipScreen(x, y, x + self.width, y + self.height)

        firstLine = self.ywin // self.font.height
        lastLine = (self.height + self.ywin) // self.font.height + 1

        curY = y - self.ywin % self.font.height
        for line in self.text[firstLine:lastLine]:
            self.font.Print(x, curY, line)
            curY += self.font.height

        ika.Video.ClipScreen()

class ScrollableTextFrame(Frame):
    '''
    Simple combination of ScrollableTextLabel and Frame
    Most of the work here is making the class behave both like a ScrollableTextLabel and
    a Frame at the same time.
    '''

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

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

# unique object returned when the user cancels a menu.
# this object's identity is its only attribute, like None.
Cancel = object()

class Menu(Widget):
    '''
    A menu.  A list of textual options displayed in some sort of text container,
    with a cursor that responds to user input, allowing the user to select an option.

    I'll readily admit that this is somewhat limiting.  Doing a SoM style ring menu with
    this class is not very realistic, but it could be implemented as its own class. (and
    probably should, considering how different it is from this.
    '''
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args)
        self.textCtrl = kwargs.get('textctrl') or ScrollableTextLabel()
        self.cursor = kwargs.get('cursor') or default_cursor
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
                    unpress = True
            elif controls.down() and self.cursorPos < len(self.Text) - 1:
                if not unpress:
                    self.cursorPos += 1
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

class Spacer(object):
    'Non-widget.  Use this to make gaps between children of a layout manager.'
    def __init__(self, width = 0, height = 0):
        self.X, self.Y = 0, 0
        self.Width, self.Height= width, height

    Right = property(lambda self: self.X + self.Width)
    Bottom = property(lambda self: self.Y + self.Height)

    def draw(self, *args):
        pass

class Layout(object):
    def __init__(self, *args):
        self.children = list(args)
        self.x = self.y = 0
        self.width = self.height = 0

    def setX(self, value):
        for child in self.children:
            child.X += value - self.x
        self.x = value

    def setY(self, value):
        for child in self.children:
            child.Y += value - self.y
        self.y = value

    def setPosition(self, p):
        (x, y) = p
        for child in self.children:
            child.X += x - self.x
            child.Y += y - self.y
        self.x, self.y = x, y

    X = property(lambda self: self.x, setX)
    Y = property(lambda self: self.y, setY)
    Left = X
    Top = Y
    Right = property(lambda self: self.x + self.width)
    Bottom = property(lambda self: self.y + self.height)
    Position = property(lambda self: (self.x, self.y), setPosition)
    Width = property(lambda self: self.width)
    Height = property(lambda self: self.height)
    Size = property(lambda self: (self.width, self.height))

    def addChild(self, child):
        assert child not in self.children, '%o is already a child!' % child
        self.children.append(child)

    def removeChild(self, child):
        assert child in self.children, '%o is not a cihld!' % child
        self.children.remove(child)

    def setChildren(self, children):
        self.children = children[:]

    def addChildren(self, children):
        self.children.extend(children)

    def removeAllChildren(self):
        self.children = []

    def draw(self, xoffset = 0, yoffset = 0):
        for child in self.children:
            child.draw(xoffset, yoffset)

class VerticalBoxLayout(Layout):
    'Arranges its children in a vertical column.'
    def __init__(self, *args, **kwargs):
        Layout.__init__(self, *args)
        self.pad = kwargs.get('pad', 0)

    def layout(self):
        y = self.y
        for child in self.children:
            if (isinstance(child, Layout)):
                child.layout()

            child.Position = (self.x, y)
            y += child.Height + self.pad

        self.width = max([child.Width + self.pad for child in self.children]) - self.pad - self.x
        self.height = y - self.y - self.pad

class HorizontalBoxLayout(Layout):
    'Arranges its children in a horizontal row.'
    def __init__(self, *args, **kwargs):
        Layout.__init__(self, *args)
        self.pad = kwargs.get('pad', 0)

    def layout(self):
        x = self.x
        for child in self.children:
            if (isinstance(child, Layout)):
                child.layout()

            child.Position = (x, self.y)
            x += child.Width + self.pad

        self.width = x - self.x
        self.height = max([child.Height + self.pad for child in self.children]) - self.pad - self.y

class FlexGridLayout(Layout):
    '''
    More robust GridLayout.  Each row/column is as big as it needs to be.  No
    bigger.
    '''
    def __init__(self, cols, *args, **kwargs):
        Layout.__init__(self, *args)
        self.cols = cols
        self.pad = kwargs.get('pad', 0)

    def layout(self):
        for child in self.children:
            if isinstance(child, Layout):
                child.layout()

        # create a 2D matrix to hold widgets for each column
        cols = [[] for x in range(self.cols)]
        for i, child in enumerate(self.children):
            cols[i % self.cols].append(child)

        # Get the widest child in each column
        rowWidths = [
            max([cell.Width + self.pad for cell in col])
            for col in cols
            ]

        # get the tallest child in each row
        colSize = len(cols[0]) # cols[0] will always be the biggest column
        colHeights = [
                max([cell.Height + self.pad for cell in
                        [col[rowIndex] for col in cols if rowIndex < len(col)]
                    ])
                for rowIndex in range(colSize)
            ]

        row, col = 0, 0
        x, y = 0, 0
        for child in self.children:
            child.Position = x + self.x, y + self.y
            x += rowWidths[col]
            col += 1
            if col >= self.cols:
                x, y = 0, y + colHeights[row]
                row, col = row + 1, 0

        self.width = max([child.Right for child in self.children]) - self.pad - self.x
        self.height = max([child.Bottom for child in self.children]) - self.pad - self.y

