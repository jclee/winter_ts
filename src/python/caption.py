import ika
import system
from thing import Thing

class Caption(Thing):

    def __init__(self, text, x = None, y = None, duration=200):
        font = system.engineObj.font

        width = font.StringWidth(text)
        height = font.height

        if x is None:   self.x = (ika.Video.xres - width) // 2
        else:           self.x = x

        if y is None:   self.y = ika.Video.yres - height - 40
        else:           self.y = y

        # TODO - make work
        #canv = ika.Canvas(width, height)
        #canv.DrawText(font, 0, 0, text)

        #self.img = ika.Image(canv)
        self.opacity = 0
        self.duration = duration
        self._updateGen =  self._update()
        self.update = lambda: next(self._updateGen)

    def _update(self):
        while self.opacity < 256:
            self.opacity += 2
            yield None

        while self.duration > 0:
            self.duration -= 1
            yield None

        while self.opacity > 0:
            self.opacity -= 2
            yield None

        yield True # seppuku

    def draw(self):
        o = min(255, self.opacity)
        # TODO: make work
        #ika.Video.TintBlit(self.img, self.x, self.y, ika.RGB(255, 255, 255, o))
