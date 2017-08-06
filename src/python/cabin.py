import ika
import controls
import savedata
import system

from xi import gui
from xi.misc import WrapText
from xi.scrolltext import ScrollableTextFrame
import xi.effects

#------------------------------------------------------------------------------

controls.init()

class Tinter(object):
    def __init__(self):
        self.curTint = 0
        self.tint = 0
        self.time = 0

    def draw(self):
        self.curTint += self.curTint < self.tint
        self.curTint -= self.curTint > self.tint

        if self.curTint:
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, self.curTint), True)

tint = Tinter()

crap = [tint] # crap to draw along with the map

def draw():
    ika.Map.Render()
    for c in crap:
        c.draw()

#------------------------------------------------------------------------------

def textBox(where, txt):
    # where is either a point or an entity
    WIDTH = 200
    width = WIDTH
    text = WrapText(txt, width, gui.default_font)
    width = max([gui.default_font.StringWidth(s) for s in text])
    height = len(text) * gui.default_font.height

    if isinstance(where, ika.Entity):
        ent = where
        x, y = ent.x + ent.hotwidth / 2 - ika.Map.xwin, ent.y - ika.Map.ywin
    else:
        x, y = where

    if x < ika.Video.xres / 2:
        x -= width / 2

    width = WIDTH
    if x + width + 16 > ika.Video.xres:
        text = WrapText(txt, ika.Video.xres - x - 16, gui.default_font)
        width = max([gui.default_font.StringWidth(s) for s in text])
        height = len(text) * gui.default_font.height

    frame = ScrollableTextFrame()
    frame.addText(*text)
    frame.autoSize()

    if y > ika.Video.yres / 2:
        y += 32
    else:
        y -= frame.Height + 16

    frame.Position = x, y
    return frame

#------------------------------------------------------------------------------

def textTask(where, txt):
    """Displays a text frame.

    Where can be either a point or an ika entity.
    """
    frame = textBox(where, txt)

    while not controls.attack():
        draw()
        frame.draw()
        ika.Video.ShowPage()
        yield from ika.Input.UpdateTask()

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

def animate(ent, frames, delay, thing=None, loop=True, text=None):
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(ent, text)
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
def sceneTask(name):
    global grandpa, kid1, kid2, kid3
    savedPos = [(e.x, e.y) for e in system.engineObj.entities]
    # hide 'em all
    for e in system.engineObj.entities:
        e.x, e.y = -100, -100

    ika.Map.Switch('maps/cabinmap.ika-map')
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']

    yield from xi.effects.fadeInTask(100)

    yield from _scenes[name]()
    setattr(savedata, name, 'True')

    yield from xi.effects.fadeOutTask(100)

    #grandpa = kid1 = kid2 = kid3 = None

    ## FIXME? AutoExec will be called when you do this!
    #if system.engineObj.mapName:
    #    ika.Map.Switch('maps/' + system.engineObj.mapName)
    #    for e, pos in zip(system.engineObj.entities, savedPos):
    #        e.x, e.y = pos

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

speech = textTask
def narration(t):
    yield from animate(grandpa, TALKING, 25, text=t)

#------------------------------------------------------------------------------
# Scenes
#------------------------------------------------------------------------------

def intro():
    yield from speech(kid1, 'Tell us a story!')
    yield from animate(kid2, (1,), delay=10, text='Yeah, the one about the ice man!')
    yield from animate(kid3, (0, 1), delay=20, text="Yeah!!")
    yield from speech(grandpa, "Isn't that story a little scary?")
    yield from speech(kid1, 'No!')
    yield from speech(kid2, 'Please tell us!')
    yield from speech(grandpa, 'Oh all right.  Ahem.')
    yield from animate(kid3, (0, 1), delay=20, text="I'm scared!!")

    tint.tint = 200

    yield from narration("""\
Across the frozen hills of Kuladriat, hunters pursue a man like any other \
prey.  Ever-northward their prey runs, till at last, at the foot of Mount \
Durinar, a chasm of ice confronts him.""")

    yield from narration("""\
The crack of a bow sounds across the vale; an instant later its arrow burying \
itself in the leg of the hunted man.  His legs buckle beneath him, and he \
tumbles down the cold ravine--""")

    yield from narration("""--the sound of stone 'gainst stone resounding.""")
    
    tint.tint = 0

    yield from narration("""\
A sharp whistle signifies the hunt's end.  The hunters will not bother \
to claim their prize, for it is far too cold--his fate is come.""")


def nearend():
    
    tint.tint = 200
    
    yield from narration("""\
As he neared his journey's end, he grew tired, and cold, and hungry.""")

    yield from narration("""He was willing to do anything to make such neverending \
misery cease, once and for all.""")

    yield from narration("""\
He considered... going back from whence he came, then.""")

    yield from narration("""But, if he were to do so, he would then have to face the \
same trials which had taken such a weary toll on his spirit to begin with.""")

    tint.tint = 0
    
    yield from speech(kid1, 'Did he go back?')
    yield from speech(kid2, 'Yeah!')
    yield from speech(kid3, "No way! He's way too brave!! Yeah!!")
    
    yield from narration("""\
In the end, no one knows whether he attempted to return... all that is important \
is the outcome.""")

    yield from narration("""But should he have gone back, he would have found the greatest reward \
of all.  Not peace... and not relief... but courage.  The courage to continue again.""")


#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
addScene(nearend)
