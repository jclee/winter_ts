import ika
from thing import Thing

class Camera(Thing):
    def __init__(self, engineRef):
        super(Camera, self).__init__()
        self.engineRef = engineRef
        self.locked = False

    def update(self):
        if not self.locked:
            x = self.engineRef.player.x - ika.Video.xres // 2
            y = self.engineRef.player.y - ika.Video.yres // 2

            ywin = ika.Map.ywin
            xwin = ika.Map.xwin

            if y > ywin: ywin += 1
            if y < ywin: ywin -= 1
            if x > xwin: xwin += 1
            if x < xwin: xwin -= 1

            ika.Map.ywin = ywin
            ika.Map.xwin = xwin

    def center(self):
        ika.Map.xwin = self.engineRef.player.x - ika.Video.xres // 2
        ika.Map.ywin = self.engineRef.player.y - ika.Video.yres // 2
