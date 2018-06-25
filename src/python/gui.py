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

default_font = ika.Font('system.fnt')

class ImageCursor(object):
    def __init__(self, filename, hotspot = None):
        img = ika.Image(filename)
        self._img = img
        self.hotspot = hotspot or (img.width, img.height // 2)

    def getWidth(self):
        return self._img.width
    def getHeight(self):
        return self._img.height

    def draw(self, x, y):
        ika.Video.Blit(self._img, x - self.hotspot[0], y - self.hotspot[1])

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

    def setX(self, value): self.x = value
    def setY(self, value): self.y = value
    def getX(self): return self.x
    def getY(self): return self.y

    def setWidth(self, value):
        assert value > 0, 'Width must be positive!! (%i)' % value
        self.width = value
    def getWidth(self): return self.width

    def setHeight(self, value):
        assert value > 0, 'Height must be positive!!! (%i)' % value
        self.height = value
    def getHeight(self):
        return self.height

    def getRight(self):
        return self.x + self.width
    def setRight(self, value):
        self.x = value - self.width

    def getBottom(self):
        return self.y + self.height
    def setBottom(self, value):
        self.y = value - self.height

    def getPosition(self):
        return (self.x, self.y)
    def setPosition(self, value):
        self.setX(value[0])
        self.setY(value[1])

    def getBorder(self):
        return self.border
    def setBorder(self, value):
        self.border = value

    def stretchHorizontally(self, x1, x2):
        assert x1 < x2, 'x1 (%i) must be smaller than x2! (%i)' % (x1, x2)
        self.setX(x1)
        self.setWidth(x2 - x1)

    def stretchVertically(self, y1, y2):
        assert y1 < y2, 'y1 (%i) must be smaller than y2! (%i)' % (y1, y2)
        self.setY(y1)
        self.setHeight(y2 - y1)

    def dockTop(self):
        self.setY(self.getBorder())
        return self

    def dockBottom(self):
        self.setBottom(ika.Video.yres - self.getBorder())
        return self

    def dockLeft(self):
        self.setX(self.getBorder())
        return self

    def dockRight(self):
        self.setRight(ika.Video.xres - self.getBorder())
        return self

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

    def autoSize(self):
        '''
        Sets the size of the frame such that every child will be visibly contained within it.
        '''
        self.width = 1
        self.height = 1
        for child in self.children:
            self.width = max(self.width, child.getWidth() + child.getX())
            self.height = max(self.height, child.getHeight() + child.getY())

class Frame(Widget):
    '''
    A widget that appears as a graphical frame of some sort.
    Frames are most commonly used as container widgets.
    '''
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        Widget.__init__(self, x, y, width, height)
        self.wnd = Window()

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

        self.font = default_font

        self.autoSize()

    def getText(self):
        return self.text
    def setText(self, value):
        self.text = value[:]

    def addText(self, text):
        'Appends text to what is already stored'
        self.text.extend(text)

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
            self.width = 1
            self.height = 1

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
        Frame.__init__(self, x, y, width, height)

        # way cool.  since keyword arguments are passed on, the font will be set properly.
        # additionally, text will be added just like StaticText.  Consistency totally rules.
        self.text = StaticText(0, 0, width, height, *args, **kwargs)

        self.addChild(self.text)
        self.autoSize()

    def getText(self):
        return self.text.getText()
    def setText(self, text):
        self.text.setText(text)

    def addText(self, text):
        'Appends text to what is already contained.'

        self.text.addText(text)

    def autoSize(self):
        'Autosizes the frame such that it is just large enough to contain its text.'
        self.text.autoSize()
        self.setWidth(self.text.getWidth())
        self.setHeight(self.text.getHeight())

class Picture(Widget):
    '''
    A widget that takes the shape of an image.
    Little else to say.
    '''
    def __init__(self, img):
        Widget.__init__(self, 0, 0, 0, 0)
        self._img = ika.Image(img)
        self.setWidth(self._img.width)
        self.setHeight(self._img.height)

    def draw(self, xoffset = 0, yoffset = 0):
        ika.Video.ScaleBlit(self._img, self.x + xoffset, self.y + yoffset, self.width, self.height)

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

    def getYWin(self):
        return self.ywin
    def setYWin(self, value):
        self.ywin = min(self.ymax - self.height, value)
        if self.ywin < 0:
            self.ywin = 0

    def getText(self):
        return self.text
    def setText(self, value):
        self.text = value[:]
        self.ymax = len(self.text) * self.font.height

    def addText(self, text):
        StaticText.addText(self, text)
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

    def __init__(self):
        Frame.__init__(self)

        self.text = ScrollableTextLabel()
        self.font = self.text.font
        self.addChild(self.text)

    def getYWin(self):
        return self.text.getYWin()
    def setYWin(self, value):
        self.text.setYWin(value)
    def getText(self):
        return self.text.getText()
    def setText(self, value):
        self.text.setText(value)

    def addText(self, text):
        self.text.addText(text)

    def autoSize(self):
        self.text.autoSize()
        self.setWidth(self.text.getWidth())
        self.setHeight(self.text.getHeight())

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
        self.cursor = ImageCursor('gfx/ui/pointer.png', hotspot=(14, 6))
        self.cursorY = 0
        self.cursorPos = 0
        self.cursorSpeed = 2 # speed at which the cursor moves (in pixels per update)
        self.addChild(self.textCtrl)

    def getWidth(self):
        return self.width
    def setWidth(self, value):
        self.width = value
        self.textCtrl.setWidth(value - self.cursor.getWidth())

    def getHeight(self):
        return self.height
    def setHeight(self, value):
        self.height = value
        self.textCtrl.setHeight(value)

    def getText(self):
        return self.textCtrl.getText()
    def setText(self, value):
        self.textCtrl.setText(value)

    def getBorder(self):
        return self.textCtrl.getBorder()
    def setBorder(self, value):
        self.textCtrl.setBorder(value)

    def addText(self, text):
        self.textCtrl.addText(text)

    def autoSize(self):
        w = self.cursor.getWidth()
        self.textCtrl.setPosition((w, 0))
        self.textCtrl.autoSize()
        self.setWidth(self.textCtrl.getWidth() + w)
        self.setHeight(self.textCtrl.getHeight())

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
        fontHeight = self.textCtrl.font.height
        ymax = max(0, len(self.getText()) * fontHeight - self.textCtrl.getHeight())
        assert 0 <= self.cursorPos <= len(self.getText()), 'cursorPos out of range 0 <= %i <= %i' % (self.cursorPos, len(self.getText()))

        delta = self.cursorPos * fontHeight - self.textCtrl.getYWin() - cy
        if delta > 0:
            if cy < self.textCtrl.getHeight() - fontHeight:
                self.cursorY += self.cursorSpeed
            else:
                self.textCtrl.setYWin(self.textCtrl.getYWin() + self.cursorSpeed)
        elif delta < 0:
            if cy > 0:
                self.cursorY -= self.cursorSpeed
            elif self.textCtrl.getYWin() > 0:
                self.textCtrl.setYWin(self.textCtrl.getYWin() - self.cursorSpeed)
        else:
            # Maybe this isn't a good idea.  Maybe it is.
            # only move the cursor if delta is zero
            # that way movement doesn't get bogged
            # down by a cursor that moves too slowly
            if controls.up() and self.cursorPos > 0:
                if not unpress:
                    self.cursorPos -= 1
                    unpress = True
            elif controls.down() and self.cursorPos < len(self.getText()) - 1:
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
        fontHeight = self.textCtrl.font.height
        self.cursor.draw(
            self.x + self.textCtrl.x + xoffset,
            self.y + self.textCtrl.y + yoffset + self.cursorY + (fontHeight // 2)
            )

class Spacer(object):
    'Non-widget.  Use this to make gaps between children of a layout manager.'
    def __init__(self, width = 0, height = 0):
        self.setX(0)
        self.setY(0)
        self.setWidth(width)
        self.setHeight(height)

    def setPosition(self, p):
        (self.x, self.y) = p

    def setX(self, value):
        self.x = value
    def getX(self):
        return self.x
    def setY(self, value):
        self.y = value
    def getY(self):
        return self.y
    def setWidth(self, value):
        self.width = value
    def getWidth(self):
        return self.width
    def setHeight(self, value):
        self.height = value
    def getHeight(self):
        return self.height

    def getRight(self):
        return self.getX() + self.getWidth()
    def getBottom(self):
        return self.getY() + self.getHeight()

    def draw(self, *args):
        pass

class Layout(object):
    def __init__(self, *args):
        self.children = list(args)
        self.x = self.y = 0
        self.width = self.height = 0

    def getX(self):
        return self.x
    def setX(self, value):
        for child in self.children:
            child.setX(child.getX() + value - self.x)
        self.x = value

    def getY(self):
        return self.y
    def setY(self, value):
        for child in self.children:
            child.setY(child.getY() + value - self.y)
        self.y = value

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getPosition(self):
        return (self.x, self.y)
    def setPosition(self, p):
        (x, y) = p
        for child in self.children:
            child.setX(child.getX() + x - self.x)
            child.setY(child.getY() + y - self.y)
        self.x, self.y = x, y

    def addChild(self, child):
        assert child not in self.children, '%o is already a child!' % child
        self.children.append(child)

    def setChildren(self, children):
        self.children = children[:]

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

            child.setPosition((self.x, y))
            y += child.getHeight() + self.pad

        self.width = max([child.getWidth() + self.pad for child in self.children]) - self.pad - self.x
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

            child.setPosition((x, self.y))
            x += child.getWidth() + self.pad

        self.width = x - self.x
        self.height = max([child.getHeight() + self.pad for child in self.children]) - self.pad - self.y

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
            max([cell.getWidth() + self.pad for cell in col])
            for col in cols
            ]

        # get the tallest child in each row
        colSize = len(cols[0]) # cols[0] will always be the biggest column
        colHeights = [
                max([cell.getHeight() + self.pad for cell in
                        [col[rowIndex] for col in cols if rowIndex < len(col)]
                    ])
                for rowIndex in range(colSize)
            ]

        row, col = 0, 0
        x, y = 0, 0
        for child in self.children:
            child.setPosition((x + self.x, y + self.y))
            x += rowWidths[col]
            col += 1
            if col >= self.cols:
                x, y = 0, y + colHeights[row]
                row, col = row + 1, 0

        self.width = max([child.getRight() for child in self.children]) - self.pad - self.x
        self.height = max([child.getBottom() for child in self.children]) - self.pad - self.y

class Window(object):
    '''
    Specialized xi window.  The only real differences are that it pulls
    its images from separate image files instead of cutting up a single
    image.
    '''
    def __init__(self):
        self.iTopleft = ika.Image('gfx/ui/win_top_left.png')
        self.iTopright = ika.Image('gfx/ui/win_top_right.png')
        self.iBottomleft = ika.Image('gfx/ui/win_bottom_left.png')
        self.iBottomright = ika.Image('gfx/ui/win_bottom_right.png')
        self.iLeft = ika.Image('gfx/ui/win_left.png')
        self.iRight = ika.Image('gfx/ui/win_right.png')
        self.iTop = ika.Image('gfx/ui/win_top.png')
        self.iBottom = ika.Image('gfx/ui/win_bottom.png')
        self.iCentre = ika.Image('gfx/ui/win_background.png')

    def draw(self, x, y, w, h):
        x2 = x + w
        y2 = y + h

        ika.Video.Blit(self.iTopleft,  x - self.iTopleft.width, y - self.iTopleft.height)
        ika.Video.Blit(self.iTopright, x2, y - self.iTopright.height)
        ika.Video.Blit(self.iBottomleft, x - self.iBottomleft.width, y2)
        ika.Video.Blit(self.iBottomright, x2, y2)

        ika.Video.ScaleBlit(self.iLeft, x - self.iLeft.width, y, self.iLeft.width, y2 - y)
        ika.Video.ScaleBlit(self.iRight, x2, y, self.iRight.width, y2 - y)

        ika.Video.ScaleBlit(self.iTop, x, y - self.iTop.height, x2 - x, self.iTop.height)
        ika.Video.ScaleBlit(self.iBottom, x, y2, x2 - x, self.iBottom.height)

        ika.Video.ScaleBlit(self.iCentre, x, y, x2 - x, y2 - y)
