import ika

# base class (abstract)
class Cursor(object):
    def __init__(self):
        self.hotspot = 0,0

    def setHotSpot(self, p):
        (x, y) = p
        self.hotspot = int(x), int(y)

    Width = property(lambda self: None)
    Height = property(lambda self: None)
    Size = property(lambda self: (self.Width, self.Height))
    HotSpot = property(lambda self: self.hotspot, setHotSpot)

    def draw(self, x, y):
        assert False, "Cursor.draw method not overloaded!";

# Basic cursor class that uses a font string as a cursor
class TextCursor(Cursor):
    def __init__(self, font, t = '>'):
        Cursor.__init__(self)

        self.width = font.StringWidth(t)
        self.height = font.height
        self.hotspot = self.width, self.height // 2

        c = ika.Canvas(self.width, self.height)
        c.DrawText(font, 0, 0, t)
        self.img = ika.Image(c)

    Width = property(lambda self: self.width)
    Height = property(lambda self: self.height)

    def draw(self, x, y):
        ika.Video.Blit(self.img, x - self.hotspot[0], y - self.hotspot[1])

class ImageCursor(Cursor):
    def __init__(self, img, hotspot = None):
        Cursor.__init__(self)
        if isinstance(img, str):
            img = ika.Image(img)
        self.img = img
        self.hotspot = hotspot or (img.width, img.height // 2)

    Width = property(lambda self: self.img.width)
    Height = property(lambda self: self.img.height)

    def draw(self, x, y):
        ika.Video.Blit(self.img, x - self.hotspot[0], y - self.hotspot[1])
