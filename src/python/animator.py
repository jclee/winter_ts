
class Animator(object):
    """Handles animating sprites."""

    def __init__(self, anim=None, loop=True):
        self._anim = anim
        self.count = 0
        self.curFrame = 0
        self.index = 0
        self.loop = loop
        self.kill = anim is None

    def __repr__(self):
        return `(
            self._anim,
            self.count,
            self.curFrame,
            self.index,
            self.loop,
            self.kill)`

    anim = property(lambda self: self._anim)

    def setAnim(self, value, loop=True):
        self._anim = value
        self.curFrame = self._anim[0][0]
        self.count = self._anim[0][1]
        self.index = 0
        self.kill = False
        self.loop = loop

    def update(self, time_delta):
        if self.kill:
            return

        self.count -= time_delta
        while self.count <= 0:
            self.index += 1
            if self.index >= len(self.anim):
                if self.loop:
                    self.index = 0
                else:
                    self.kill = True
                    return

            self.curFrame = self.anim[self.index][0]
            self.count += self.anim[self.index][1]

    def stop(self):
        self.kill = True

    def resume(self):
        self.kill = False
        if self.index >= len(self.anim):
            self.restart()

    def restart(self):
        self.index = 0
        self.count = 0
        self.kill = False


def makeAnim(strand, delay):
    """Quicky function to make a proper strand, given a
       list of frames, and a delay between each."""

    return zip(strand, [delay] * len(strand))
