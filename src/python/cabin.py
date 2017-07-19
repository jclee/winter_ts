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

def text(where, txt):
    """Displays a text frame.

    Where can be either a point or an ika entity.
    """
    frame = textBox(where, txt)

    while not controls.attack():
        draw()
        frame.draw()
        ika.Video.ShowPage()
        ika.Input.Update()

#------------------------------------------------------------------------------

def animate(ent, frames, delay, thing=None, loop=True, text=None):
    class AnimException(Exception):
        pass
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(ent, text)
        crap.append(text)
    try:
        while True:
            for frame in frames:
                ent.specframe = frame
                d = delay
                while d > 0:
                    d -= 1
                    draw()
                    ika.Video.ShowPage()
                    ika.Delay(1)
                    ika.Input.Update()
                    if controls.attack():
                        loop = False
                        raise AnimException
            if not loop:
                raise AnimException
    except:  #except what?
        if thing:
            crap.remove(thing)
        if text:
            crap.remove(text)
        ent.specframe = 0

#------------------------------------------------------------------------------
# Scene code
#------------------------------------------------------------------------------

_scenes = {}

# TODO: transitions
def scene(name):
    global grandpa, kid1, kid2, kid3
    savedPos = [(e.x, e.y) for e in system.engine.entities]
    # hide 'em all
    for e in system.engine.entities:
        e.x, e.y = -100, -100

    ika.Map.Switch('maps/cabinmap.ika-map')
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']

    xi.effects.fadeIn(100)

    _scenes[name]()
    setattr(savedata, name, 'True')

    xi.effects.fadeOut(100)

    grandpa = kid1 = kid2 = kid3 = None

    # FIXME? AutoExec will be called when you do this!
    if system.engine.mapName:
        ika.Map.Switch('maps/' + system.engine.mapName)
        for e, pos in zip(system.engine.entities, savedPos):
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

speech = text
narration = lambda t: animate(grandpa, TALKING, 25, text=t)

#------------------------------------------------------------------------------
# Scenes
#------------------------------------------------------------------------------

def fake_scene_1():
    speech(grandpa, "Listen kids, for in my drunken stupour, I shall tell a tale like none you've ever heard!")
    speech(grandpa, '*hic*')
    speech(kid1, 'All right!  Alchohol induced ranting!')
    speech(kid2, 'COCKS')
    speech(kid3, 'POTTYMOUTH')
    speech(kid2, 'You just shut the fuck up, freak!')
    speech(kid3, ':(')
    speech(grandpa, 'And thus, the world exploded.')


def fake_intro():
    speech(grandpa, 'Heeeeey kids!')
    speech(grandpa, "Sit back, fuckers, 'cause I'm gonna tell you a story, and you're going enjoy it whether you want to or not.")
    speech(kid1, '....')
    speech(kid2, 'Who are you, and what are you doing in our house?')
    animate(kid3, (0, 1), delay=20,
        text="PLEASE DON'T RAPE ME"
    )
    animate(grandpa, (6, 0, 7, 0), delay=100,
        text='The curse compels me to rant about shit you do not care about to atone for my previous child molestations.'
    )
    speech(kid2, 'HURRAY STORY TIME')
    speech(kid1, 'Tell us a story about ramming your old wrinkly dick in baby orofices!')

    speech(grandpa, 'It was a dark and stormy night!')
    speech(grandpa, 'Perfect for a night on the town.')
    speech(grandpa, 'Except that, as a child molester, I had to live far away from town.')
    speech(kid3, 'OMG')
    speech(grandpa, 'So, anyway, there I was in the middle of nowhere, off to town so I could find somewhere cozy to hide my cock....')


def intro():
    speech(kid1, 'Tell us a story!')
    animate(kid2, (1,), delay=10, text='Yeah, the one about the ice man!')
    animate(kid3, (0, 1), delay=20, text="Yeah!!")
    speech(grandpa, "Isn't that story a little scary?")
    speech(kid1, 'No!')
    speech(kid2, 'Please tell us!')
    speech(grandpa, 'Oh all right.  Ahem.')
    animate(kid3, (0, 1), delay=20, text="I'm scared!!")

    tint.tint = 200

    narration("""\
Across the frozen hills of Kuladriat, hunters pursue a man like any other \
prey.  Ever-northward their prey runs, till at last, at the foot of Mount \
Durinar, a chasm of ice confronts him.""")

    narration("""\
The crack of a bow sounds across the vale; an instant later its arrow burying \
itself in the leg of the hunted man.  His legs buckle beneath him, and he \
tumbles down the cold ravine--""")

    narration("""--the sound of stone 'gainst stone resounding.""")
    
    tint.tint = 0

    narration("""\
A sharp whistle signifies the hunt's end.  The hunters will not bother \
to claim their prize, for it is far too cold--his fate is come.""")



def impasse():
    narration("""\
The stone walls seemed to draw in closer, choking the very breath \
from him; the way was sealed.  However, as despair welled within \
him, a glint of hope shone through as light through the gelid rock.  \
If only there were some way to breach it...""")



def nearend():
    
    tint.tint = 200
    
    narration("""\
As he neared his journey's end, he grew tired, and cold, and hungry.""")

    narration("""He was willing to do anything to make such neverending \
misery cease, once and for all.""")

    narration("""\
He considered... going back from whence he came, then.""")

    narration("""But, if he were to do so, he would then have to face the \
same trials which had taken such a weary toll on his spirit to begin with.""")

    tint.tint = 0
    
    speech(kid1, 'Did he go back?')
    speech(kid2, 'Yeah!')
    speech(kid3, "No way! He's way too brave!! Yeah!!")
    
    narration("""\
In the end, no one knows whether he attempted to return... all that is important \
is the outcome.""")

    narration("""But should he have gone back, he would have found the greatest reward \
of all.  Not peace... and not relief... but courage.  The courage to continue again.""")



#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
#addScene(rune_of_water)
#addScene(rune_of_fire)
#addScene(rune_of_wind)
#addScene(impasse)
addScene(nearend)
#addScene(forebattle)
#addScene(epilogue)
