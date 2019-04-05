import ika
from thing import Thing

def sgn(i):
    if i > 0: return 1
    elif i < 0: return -1
    else: return 0

class _Gauge(Thing):
    def __init__(self, engineRef, imageName, x, y, justify = 'left'):
        '''
        imageName - name of the image series to use.
         ie 'gfx/ui/barhp%i.png'
        x,y are position
        justify is either 'left' or 'right'
        '''

        self.engineRef = engineRef
        (self.span, self.left, self.middle, self.right) =\
            [engineRef.getImage(imageName % i) for i in range(4)]
        self.oldVal = self.oldMax = 0
        self.x, self.y = x,y
        self.justify = justify.lower()
        self.opacity = 0
        self.rgb = [255, 255, 255]
        self.width = None
        self.fadeIn = False

    def update(self):
        v = sgn(self.curVal - self.oldVal)
        m = sgn(self.curMax - self.oldMax)

        if self.fadeIn:
            self.opacity = min(512, self.opacity + 20)
            if self.opacity == 512:
                self.fadeIn = False

        if not v and not m:
            self.opacity = max(0, self.opacity - 1)
        else:
            self.fadeIn = True
            self.oldVal += v
            self.oldMax += m

    def draw(self):
        if self.opacity == 0:
            return

        o = min(1.0, self.opacity / 255.0)

        # the width of the repeated span image thingo.
        # each end of the gauge occupies two pixels, so we subtract four.
        # (bad hack, I know)
        width = (self.width or self.oldMax) - 3

        if self.justify == 'left':
            x = self.x + 2
        else:
            x = ika.Video.xres - width - self.left.width - self.right.width - self.x - 2

        ika.Video.TintBlit(self.left, x, self.y, o)
        ika.Video.TintBlit(self.right, x + width + self.left.width, self.y, o)

        x += self.left.width

        ika.Video.TintScaleBlit(self.span, x, self.y, width, self.span.height, o)

        x -= 2

        if self.width:
            v = self.oldVal * self.width // self.oldMax
        else:
            v = self.oldVal

        if self.oldVal:
            if self.justify == 'left':
                self.drawRect(x, self.y + 5, x + v, self.y + 6, o)
            else:
                self.drawRect(x + (self.width or self.oldMax) - v, self.y + 5, x + (self.width or self.oldMax), self.y + 6, o)

    def drawRect(self, x, y, w, h, opacity):
        'Used to draw in the filled part of the gauge.'
        ika.Video.DrawRect(x, y, w, h, ika.RGB(*(self.rgb + [opacity])))

    curVal = property(lambda self: None) # ditto
    curMax = property(lambda self: None) # override.  Needs to be readable.

class HPBar(_Gauge):
    def __init__(self, engineRef):
        _Gauge.__init__(self, engineRef, 'gfx/ui/barhp%i.png', 0, 0, justify='right')
        self.y = ika.Video.yres - self.left.height - 1
        self.rgb = [255, 0, 0]

    curVal = property(lambda self: self.engineRef.player.stats.hp)
    curMax = property(lambda self: self.engineRef.player.stats.maxhp)

class MPBar(_Gauge):
    def __init__(self, engineRef):
        _Gauge.__init__(self, engineRef, 'gfx/ui/barhp%i.png', 0, 0, justify='right')
        self.y = ika.Video.yres - self.left.height * 2 - 1
        self.rgb = [0, 0, 255]
        self.oldMax = self.curMax
        self.oldVal = self.curVal

    curVal = property(lambda self: self.engineRef.player.stats.mp)
    curMax = property(lambda self: self.engineRef.player.stats.maxmp)

class EXPBar(_Gauge):
    def __init__(self, engineRef):
        _Gauge.__init__(self, engineRef, 'gfx/ui/barmp%i.png', 0, 0, justify='right')
        #self.y = ika.Video.yres - self.left.height * 2 - 1
        self.width = 100
        self.rgb = [0, 128, 128]
        self.oldMax = self.curMax
        self.oldVal = self.curVal

    def drawRect(self, x, y, w, h, opacity):
        super(EXPBar, self).drawRect(x, y, w, h - 1, opacity)

    curVal = property(lambda self: self.engineRef.player.stats.exp * self.width // self.engineRef.player.stats.next)
    curMax = property(lambda self: self.width)
