import ika
import snow

_text = '''\
Winter



*****



Management,
Main program
-
Andy Friesen


Artwork
-
Corey Annis


Maps
-
Corey Annis
Francis Brazeau (aka Hatchet)
Andy Friesen
Troy Potts (aka Thrasher)


Music
-
'Winter' by David Churchill (aka infey)
'Competative' by Disturbed
'Existing' by Mick Rippon
'Ressurection' (Author unknown)
'xerxes vs solo' (Author unknown)
'Lampoons Haunting' (Author Unknown)


Script
-
Ian Bollinger (aka Ear)


Additionally, everybody on the team had a
hand in the concept and layout of the
game.  You guys rock!




***




hm.... need to fill this up with some other
junk, just so that the music gets a chance
to play all the way through.
(Mick Rippon is awesome)

It's fairly safe to expect an early '04
rerelease of Winter with extra polish,
as well as more spells, skills, and general
coolness to be found.  There may or may
not be a second chapter to the story as
well.  Time will tell.

Speaking of which, there actually *is*
a story, but we didn't get time to tell
it properly.  The '04 release will remedy
this, at the very least.



Goddammit.



Going to need to put WAY more crap in
here if I'm going to meet the quota
I set forth for myself.  May as well rant
about Winter.

For those wondering, the snowfield is
implemented in C++.  It directly does things
by accessing OpenGL.  I'm quite shocked
(and pleased!) that it works as well as it
obviously does.  You can be sure I'll be doing
more experimenting with this particular
nuance of ika later on.

There are a grand total of 48 maps in the
game, but the original plan called for over
80.  A few ikaMap scripts were adapted
specifically for creating these maps.  I
was so sure we wouldn't get them all done
on time.  Thrasher, corey and Hatchet
deserve a big pat on the back for that feat
alone. (me and Ear just tweaked things
here and there)

All the AI is implemented using Python
coroutines, which allowed us to do some
funky things that would have been
extremely difficult otherwise.  While
it was still quite time consuming to
implement, I'm very pleased with the
results. :)

Okay, I think that's about enough.  If
it's *still* not enough crap to let the
song play through once, then you'll have
to take the time to play it in your mod
player of choice. (it sounds okay in
WinAmp, though it's quieter than it
ought to be)

Merry Christmas, all!

- andy -

***



























The curious shall be rewarded!

There is at least one optional,
secret spell in the game.  Thrasher
went to great lengths to make it
obscenely difficult to obtain!

'''.split('\n')

def creditsTask(engineRef):
    m = engineRef.music.get('music/Existing.s3m', ika.Sound('music/Existing.s3m'))
    m.loop = True
    engineRef.fader.kill()
    engineRef.fader.reset(m)

    vignette = engineRef.getImage('gfx/credits_vignette.png')
    bg = engineRef.getImage('gfx/mountains.png')
    snowObj = snow.Snow(velocity=(0, 1))
    y = -ika.Video.yres
    font = ika.Font('system.fnt')

    def draw():
        ika.Video.Blit(bg, 0, 0)
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128))

        firstLine = int(y) // font.height
        adjust = int(y) % font.height
        length = (ika.Video.yres // font.height) + 1

        #print(firstLine)

        Y = -adjust
        while Y < ika.Video.yres and firstLine < len(_text):
            if firstLine >= 0:
                font.CenterPrint(160, Y, _text[firstLine])
            Y += font.height
            firstLine += 1

        ika.Video.Blit(vignette, 0, 0)

        snowObj.draw()

    now = ika.GetTime()
    while True:
        t = ika.GetTime()
        delta = (t - now) / 10.0
        y += delta
        now = t
        snowObj.update()

        draw()
        ika.Video.ShowPage()
        yield None
