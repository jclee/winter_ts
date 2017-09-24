import ika
import snow

import controls

class _DoneException(Exception):
    pass

def delayTask(draw, count, snowObj):
    while count > 0:
        draw()
        snowObj.update()
        snowObj.draw()
        yield from ika.DelayTask(1)
        count -= 1
        ika.Video.ShowPage()

        ika.Input.Update()
        if controls.attack():
            raise _DoneException()

def introTask():
    snowObj = snow.Snow(velocity=(0,0.5))
    gba = ika.Image('gfx/gba.png')
    yourmom = ika.Image('gfx/yourmother.png')
    isabitch = ika.Image('gfx/isabigfatbitch.png')

    controls.attack() # unpress

    v = ika.Video
    d = 40

    def showGba():
        v.ClearScreen()
        v.Blit(gba, (v.xres - gba.width) // 2, (v.yres - gba.height) // 2)

    try:
        yield from delayTask(showGba, 300, snowObj)

        yield from delayTask(lambda: v.ClearScreen(), d, snowObj)

        for x in range(3):
            yield from delayTask(lambda: v.Blit(yourmom, 0, 0, ika.Opaque), d, snowObj)
            yield from delayTask(lambda: v.ClearScreen(), d, snowObj)

        yield from delayTask(lambda: v.Blit(isabitch, 0, 0, ika.Opaque), d // 2, snowObj)
        yield from delayTask(lambda: v.ClearScreen(), d, snowObj)
    except _DoneException:
        return

def menuTask(resultRef):
    bg = ika.Image('gfx/title.png')
    cursor = ika.Image('gfx/ui/pointer.png')
    snowObj = snow.Snow(velocity=(0, 0.5))
    snowObj.update()
    resultRef[0] = None
    cursorPos = 0
    FADE_TIME = 60

    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        ika.Video.Blit(cursor, 68, 128 + cursorPos * 26)

    for i in range(FADE_TIME - 1, -1, -1):
        draw()
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 // FADE_TIME), True)
        snowObj.update()
        snowObj.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        yield from ika.DelayTask(1)

    u = 0 # gay unpress hack

    while resultRef[0] == None:
        draw()
        snowObj.update()
        snowObj.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        yield from ika.DelayTask(1)

        if controls.up() and cursorPos > 0:
            if not u:
                cursorPos -= 1
                u = 1
        elif controls.down() and cursorPos < 2:
            if not u:
                cursorPos += 1
                u = 1
        elif controls.attack():
            resultRef[0] = cursorPos
        else:
            u = 0

    # one last draw.  Later on, there's a blurfade that can take advantage of this:
    draw()
    snowObj.draw()

    #for i in range(FADE_TIME):
    #    draw()
    #    ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 // FADE_TIME), True)
    #    snowObj.update()
    #    snowObj.draw()
    #    ika.Video.ShowPage()
    #    ika.Input.Update()
    #    yield from ika.DelayTask(1)
