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
