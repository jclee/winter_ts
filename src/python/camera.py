import ika
from thing import Thing

class Camera(Thing):
    def __init__(self, engineRef):
        super(Camera, self).__init__()
        self.engineRef = engineRef
        self.locked = False

    def update(self):
        if not self.locked:
            x = self.engineRef.player.sprite.x - self.engineRef.video.xres // 2
            y = self.engineRef.player.sprite.y - self.engineRef.video.yres // 2

            ywin = self.engineRef.map.ywin
            xwin = self.engineRef.map.xwin

            if y > ywin: ywin += 1
            if y < ywin: ywin -= 1
            if x > xwin: xwin += 1
            if x < xwin: xwin -= 1

            self.engineRef.map.ywin = ywin
            self.engineRef.map.xwin = xwin

    def center(self):
        self.engineRef.map.xwin = self.engineRef.player.sprite.x - self.engineRef.video.xres // 2
        self.engineRef.map.ywin = self.engineRef.player.sprite.y - self.engineRef.video.yres // 2
