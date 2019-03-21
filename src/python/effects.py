import ika

# Some neat-O special effects

def _blurScreen(factor):
    '''Grabs the screen, blurs it up a bit, then returns the image.
    Returns tinier images.  Use scaleblit to bring them back.

    Grossly inefficient.
    '''

    w = int(ika.Video.xres * factor)
    h = int(ika.Video.yres * factor)

    bleh = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)
    ika.Video.ScaleBlit(bleh, 0, 0, w, h)
    ika.Video.FreeImage(bleh)
    return ika.Video.GrabImage(0, 0, w, h)

def createBlurImages():
    BLEH = 1
    images = []
    i = 1.0
    while i < 2:
        img = _blurScreen(1.0 / i)
        images.append(img)
        ika.Video.ScaleBlit(img, -BLEH, -BLEH, ika.Video.xres + BLEH * 2, ika.Video.yres + BLEH * 2)

        i += 0.1

    return images

def freeBlurImages(images):
    for img in images:
        ika.Video.FreeImage(img)

def blurFadeTask(time, startImages, endImages):
    now = ika.GetTime()
    startTime = now
    endTime = now + time
    while now < endTime:
        imageIndex = (now - startTime) * len(startImages) // time
        opacity = (now - startTime) / time

        ika.Video.ScaleBlit(startImages[imageIndex], 0, 0, ika.Video.xres, ika.Video.yres)
        ika.Video.TintScaleBlit(endImages[-(imageIndex+1)], 0, 0, ika.Video.xres, ika.Video.yres, opacity)

        ika.Video.ShowPage()
        yield None
        now = ika.GetTime()

def _fadeTask(time, startAlpha, endAlpha, draw):
    deltaAlpha = endAlpha - startAlpha

    now = ika.GetTime()
    startTime = now
    endtime = now + time

    while now < endtime:
        draw()
        alpha = startAlpha + deltaAlpha * (now - startTime) / time
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, int(alpha * 255)))

        ika.Video.ShowPage()
        yield None
        now = ika.GetTime()

def fadeInTask(time, draw = ika.Map.Render):
    yield from _fadeTask(time, 1.0, 0.0, draw)

def fadeOutTask(time, draw = ika.Map.Render):
    yield from _fadeTask(time, 0.0, 1.0, draw)
