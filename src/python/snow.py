import ika

_COUNT = 10
_MAX_LIFE = 100

class Snow(object):
    def __init__(self, velocity):
        self.velocity = velocity
        self.particles = []
        for i in range(_COUNT):
            x = ika.Random(0, ika.Video.xres)
            y = ika.Random(0, ika.Video.yres)
            vx = ika.Random(-1, 2)
            self.particles.append([x, y, vx, 0])

    def update(self):
        for p in self.particles:
            p[0] += p[2]
            p[1] += 1
            p[3] += 1
            if (p[0] < 0
                    or p[0] >= ika.Video.xres
                    or p[1] >= ika.Video.yres
                    or p[3] >= _MAX_LIFE):
                p[0] = ika.Random(0, ika.Video.xres)
                p[1] = ika.Random(0, ika.Video.yres)
                p[2] = ika.Random(-1, 2)
                p[3] = 0

    def draw(self):
        for p in self.particles:
            ika.Video.DrawPixel(p[0], p[1], ika.RGB(255, 255, 255))
