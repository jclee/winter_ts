class Animator(object):
    """Handles animating sprites."""

    def __init__(self):
        self._frameIndexTimePairs = None
        self._count = 0
        self.curFrame = 0
        self.index = 0
        self._loop = True
        self.isAnimating = False

    def start(self, frameIndexTimePairs, loop):
        self._frameIndexTimePairs = frameIndexTimePairs
        self.curFrame = self._frameIndexTimePairs[0][0]
        self._count = self._frameIndexTimePairs[0][1]
        self.index = 0
        self.isAnimating = True
        self._loop = loop

    def update(self):
        if not self.isAnimating:
            return

        self._count -= 1
        while self._count <= 0:
            self.index += 1
            if self.index >= len(self._frameIndexTimePairs):
                if self._loop:
                    self.index = 0
                else:
                    self.isAnimating = False
                    return

            self.curFrame = self._frameIndexTimePairs[self.index][0]
            self._count += self._frameIndexTimePairs[self.index][1]

    def stop(self):
        self.isAnimating = False

def makeAnim(strand, delay):
    """Quicky function to make a proper strand, given a
       list of frames, and a delay between each."""

    return list(zip(strand, [delay] * len(strand)))
