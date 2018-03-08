import ika
from browser import window

class Snow(object):
    def __init__(self, count=100, velocity=(0, 0.5), colour=ika.RGB(255, 255, 255)):
        self._winterSnow = window.WinterSnow.new(
            ika.Video.xres,
            ika.Video.yres,
            count,
            velocity,
            colour,
        )

    def update(self):
        self._winterSnow.update()

    def draw(self):
        self._winterSnow.draw(ika.GetCanvasEl())
