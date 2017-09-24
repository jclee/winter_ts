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

class AnimatedCursor(Cursor):
    def __init__(self, images, delay = 10, hotspot = None):
        assert len(images) > 0, 'Need at least one animation frame. ;P'

        Cursor.__init__(self)
        self.width = images[0].width
        self.height = images[0].height
        self.hotspot = hotspot or (self.width, self.height // 2)
        self.delay = delay

        self.frames = images

    Width = property(lambda self: self.width)
    Height = property(lambda self: self.height)

    def draw(self, x, y):
        frame = ika.GetTime() // self.delay

        ika.Video.Blit(self.frames[frame % len(self.frames)],
            x - self.hotspot[0], y - self.hotspot[1])

    # static method to create a cursor by cutting frames out of one
    # big image (vertical strip)
    def createFromImageStrip(canvas, numFrames, delay = 10, hotspot = None):
        assert canvas.height % numFrames == 0, \
            "Image's height is not an even multiple of the number of frames."

        frames = [None] * numFrames
        # cut up the canvas, and create our images
        for i in range(numFrames):
            c = ika.Canvas(self.width, self.height)
            canvas.Blit(c, 0, -(i * self.height), ika.Opaque)
            frames[i] = ika.Image(c)

        return AnimatedCursor(frames, delay, hotspot)

    createFromImageStrip = staticmethod(createFromImageStrip)
