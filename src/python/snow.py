import ika
from browser import window

class Snow(object):
    def __init__(self, velocity):
        self._winterSnow = window.WinterSnow.new(
            ika.Video.xres,
            ika.Video.yres,
            velocity
        )

    def update(self):
        self._winterSnow.update()

    def draw(self):
        self._winterSnow.draw(ika.GetCanvasEl())
