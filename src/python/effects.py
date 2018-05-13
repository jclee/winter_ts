import ika

# Some neat-O special effects

def blurScreen(factor):
    '''Grabs the screen, blurs it up a bit, then returns the image.
    Returns tinier images.  Use scaleblit to bring them back.

    Grossly inefficient.
    '''

    w = int(ika.Video.xres * factor)
    h = int(ika.Video.yres * factor)

    bleh = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)
    ika.Video.ScaleBlit(bleh, 0, 0, w, h, ika.Opaque)
    return ika.Video.GrabImage(0, 0, w, h)

def createBlurImages():
    BLEH = 1
    images = []
    i = 1.0
    while i < 2:
        img = blurScreen(1.0 / i)
        images.append(img)
        ika.Video.ScaleBlit(img, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)

        ika.Video.ScaleBlit(img, -BLEH, -BLEH, ika.Video.xres + BLEH * 2, ika.Video.yres + BLEH * 2)

        i += 0.1

    return images

def blurFadeTask(time, startImages, endImages):
    startTime = ika.GetTime()
    endTime = ika.GetTime() + time
    now = startTime
    while now < endTime:
        imageIndex = (now - startTime) * len(startImages) // time
        opacity = (now - startTime) * 255 // time
        startfade = ika.RGB(255, 255, 255, 255 - opacity)
        endfade = ika.RGB(255, 255, 255, opacity)

        ika.Video.TintDistortBlit(
            startImages[imageIndex],
            (0, 0, startfade), (ika.Video.xres, 0, startfade),
            (ika.Video.xres, ika.Video.yres, startfade),
            (0, ika.Video.yres, startfade))
        ika.Video.TintDistortBlit(
            endImages[-(imageIndex+1)],
            (0, 0, endfade), (ika.Video.xres, 0, endfade),
            (ika.Video.xres, ika.Video.yres, endfade),
            (0, ika.Video.yres, endfade))

        ika.Video.ShowPage()
        yield None
        now = ika.GetTime()
