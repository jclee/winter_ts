import controls
import effects
import gui
import ika
from misc import WrapText

#------------------------------------------------------------------------------

class Tinter(object):
    def __init__(self):
        self.curTint = 0
        self.tint = 0
        self.time = 0

    def draw(self):
        self.curTint += self.curTint < self.tint
        self.curTint -= self.curTint > self.tint

        if self.curTint:
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, self.curTint))

tint = Tinter()

crap = [tint] # crap to draw along with the map

def draw():
    ika.Map.Render()
    for c in crap:
        c.draw()

#------------------------------------------------------------------------------

def textBox(engineRef, ent, txt):
    WIDTH = 200
    width = WIDTH
    text = WrapText(txt, width, gui.default_font)
    width = max([gui.default_font.StringWidth(s) for s in text])
    height = len(text) * gui.default_font.height

    x, y = ent.x + ent.hotwidth // 2 - ika.Map.xwin, ent.y - ika.Map.ywin

    if x < ika.Video.xres // 2:
        x -= width // 2

    width = WIDTH
    if x + width + 16 > ika.Video.xres:
        text = WrapText(txt, ika.Video.xres - x - 16, gui.default_font)
        width = max([gui.default_font.StringWidth(s) for s in text])
        height = len(text) * gui.default_font.height

    frame = gui.ScrollableTextFrame(engineRef)
    frame.addText(text)
    frame.autoSize()

    if y > ika.Video.yres // 2:
        y += 32
    else:
        y -= frame.getHeight() + 16

    frame.setPosition((x, y))
    return frame

#------------------------------------------------------------------------------

def speech(engineRef, where, txt):
    """Displays a text frame.

    Where can be either a point or an ika entity.
    """
    frame = textBox(engineRef, where, txt)

    while not controls.attack():
        draw()
        frame.draw()
        ika.Video.ShowPage()
        yield None

#------------------------------------------------------------------------------

def animateHelper(ent, frames, delay, loop):
    while True:
        for frame in frames:
            ent.specframe = frame
            d = delay
            while d > 0:
                d -= 1
                draw()
                ika.Video.ShowPage()
                yield from ika.DelayTask(1)
                if controls.attack():
                    return
        if not loop:
            return

def animate(engineRef, ent, frames, delay, thing=None, loop=True, text=None):
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(engineRef, ent, text)
        crap.append(text)

    yield from animateHelper(ent, frames, delay, loop)

    if thing is not None:
        crap.remove(thing)
    if text is not None:
        crap.remove(text)
    ent.specframe = 0

#------------------------------------------------------------------------------
# Scene code
#------------------------------------------------------------------------------

_scenes = {}

# TODO: transitions
def sceneTask(engineRef, name):
    global grandpa, kid1, kid2, kid3
    savedPos = [(e.x, e.y) for e in engineRef.entities]
    # hide 'em all
    for e in engineRef.entities:
        e.x, e.y = -100, -100

    ika.Map.Switch('maps/cabinmap.ika-map')
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']

    yield from effects.fadeInTask(100)

    yield from _scenes[name](engineRef)
    engineRef.saveFlags[name] = 'True'

    yield from effects.fadeOutTask(100)

    grandpa = kid1 = kid2 = kid3 = None

    if engineRef.mapName:
        # We now only call AutoExec in engine.mapSwitchTask, not
        # ika.Map.Switch, so this should be an OK way to restore the map.
        ika.Map.Switch('maps/' + engineRef.mapName)
        for e, pos in zip(engineRef.entities, savedPos):
            e.x, e.y = pos

# name : function pairs
def addScene(function):
    _scenes[function.__name__] = function

#------------------------------------------------------------------------------
# Ear's functions
#------------------------------------------------------------------------------

PAUSE = 0
SPEAKING = 1
NOD = 2

TALKING = (
    [PAUSE]*3 +
    [SPEAKING]*2 +
    [PAUSE]*3 +
    [SPEAKING]*2 +
    [PAUSE]*3 +
    [NOD]
)

def narration(engineRef, t):
    yield from animate(engineRef, grandpa, TALKING, 25, text=t)

#------------------------------------------------------------------------------
# Scenes
#------------------------------------------------------------------------------

def intro(engineRef):
    yield from speech(engineRef, kid1, 'Tell us a story!')
    yield from animate(engineRef, kid2, (1,), delay=10, text='Yeah, the one about the ice man!')
    yield from animate(engineRef, kid3, (0, 1), delay=20, text="Yeah!!")
    yield from speech(engineRef, grandpa, "Isn't that story a little scary?")
    yield from speech(engineRef, kid1, 'No!')
    yield from speech(engineRef, kid2, 'Please tell us!')
    yield from speech(engineRef, grandpa, 'Oh all right.  Ahem.')
    yield from animate(engineRef, kid3, (0, 1), delay=20, text="I'm scared!!")

    tint.tint = 200

    yield from narration(engineRef, """\
Across the frozen hills of Kuladriat, hunters pursue a man like any other \
prey.  Ever-northward their prey runs, till at last, at the foot of Mount \
Durinar, a chasm of ice confronts him.""")

    yield from narration(engineRef, """\
The crack of a bow sounds across the vale; an instant later its arrow burying \
itself in the leg of the hunted man.  His legs buckle beneath him, and he \
tumbles down the cold ravine--""")

    yield from narration(engineRef, """--the sound of stone 'gainst stone resounding.""")
    
    tint.tint = 0

    yield from narration(engineRef, """\
A sharp whistle signifies the hunt's end.  The hunters will not bother \
to claim their prize, for it is far too cold--his fate is come.""")


def nearend(engineRef):
    
    tint.tint = 200
    
    yield from narration(engineRef, """\
As he neared his journey's end, he grew tired, and cold, and hungry.""")

    yield from narration(engineRef, """He was willing to do anything to make such neverending \
misery cease, once and for all.""")

    yield from narration(engineRef, """\
He considered... going back from whence he came, then.""")

    yield from narration(engineRef, """But, if he were to do so, he would then have to face the \
same trials which had taken such a weary toll on his spirit to begin with.""")

    tint.tint = 0
    
    yield from speech(engineRef, kid1, 'Did he go back?')
    yield from speech(engineRef, kid2, 'Yeah!')
    yield from speech(engineRef, kid3, "No way! He's way too brave!! Yeah!!")
    
    yield from narration(engineRef, """\
In the end, no one knows whether he attempted to return... all that is important \
is the outcome.""")

    yield from narration(engineRef, """But should he have gone back, he would have found the greatest reward \
of all.  Not peace... and not relief... but courage.  The courage to continue again.""")


#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
addScene(nearend)
