import ika
from thing import Thing

class Caption(Thing):

    def __init__(self, engineRef, font, text, x = None, y = None, duration=200):
        self.engineRef = engineRef
        self.font = font

        width = self.font.StringWidth(text)
        height = self.font.height

        if x is None:   self.x = (self.engineRef.video.xres - width) // 2
        else:           self.x = x

        if y is None:   self.y = self.engineRef.video.yres - height - 40
        else:           self.y = y

        self.text = text
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
        self.font.PrintWithOpacity(self.x, self.y, self.text, o)
