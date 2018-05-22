# Basic layout management classes
# coded by Andy Friesen
# copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.
#
# All glory to the list comprehension.

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
