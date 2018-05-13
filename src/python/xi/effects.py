# Gaudy eye candy.
# coded by Andy Friesen
# copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.

import ika

def fadeTask(time, startColour = ika.RGB(0, 0, 0, 0), endColour = ika.RGB(0, 0, 0, 255), draw = ika.Map.Render):
    startColour = ika.GetRGB(startColour)
    endColour   = ika.GetRGB(endColour)
    deltaColour = [ s - e for e, s in zip(startColour, endColour) ]

    t = ika.GetTime()
    endtime = t + time
    saturation = 0.0

    while t < endtime:
        i = ika.GetTime() - t
        t = ika.GetTime()
        saturation = min(saturation + float(i) / time, 1.0)
        draw()
        colour = [int(a + b * saturation) for a, b in zip(startColour, deltaColour)]

        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
            ika.RGB(*colour),
            True)

        ika.Video.ShowPage()
        yield None

def fadeInTask(time, colour = ika.RGB(0, 0, 0), draw = ika.Map.Render):
    yield from fadeTask(time, colour, ika.RGB(0, 0, 0, 0), draw)

def fadeOutTask(time, colour = ika.RGB(0, 0, 0), draw = ika.Map.Render):
    yield from fadeTask(time, ika.RGB(0, 0, 0, 0), colour, draw)
