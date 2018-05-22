import ika

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
