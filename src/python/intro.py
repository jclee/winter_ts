import ika
from snow import Snow

import controls

class _DoneException(Exception):
    pass

def delay(draw, count, snow):
    while count > 0:
        draw()
        snow.update()
        snow.draw()
        ika.Delay(1)
        count -= 1
        ika.Video.ShowPage()

        ika.Input.Update()
        if controls.attack():
            raise _DoneException()

def intro():
    snow = Snow(velocity=(0,0.5))
    gba = ika.Image('gfx/gba.png')
    yourmom = ika.Image('gfx/yourmother.png')
    isabitch = ika.Image('gfx/isabigfatbitch.png')

    controls.attack() # unpress

    v = ika.Video
    d = 40

    def showGba():
        v.ClearScreen()
        v.Blit(gba, (v.xres - gba.width) / 2, (v.yres - gba.height) / 2)

    try:
        delay(showGba, 300, snow)

        delay(lambda: v.ClearScreen(), d, snow)

        for x in range(3):
            delay(lambda: v.Blit(yourmom, 0, 0, ika.Opaque), d, snow)
            delay(lambda: v.ClearScreen(), d, snow)

        delay(lambda: v.Blit(isabitch, 0, 0, ika.Opaque), d / 2, snow)
        delay(lambda: v.ClearScreen(), d, snow)
    except _DoneException:
        return

def menu():
    bg = ika.Image('gfx/title.png')
    cursor = ika.Image('gfx/ui/pointer.png')
    snow = Snow(velocity=(0, 0.5))
    snow.update()
    result = None
    cursorPos = 0
    FADE_TIME = 60

    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        ika.Video.Blit(cursor, 68, 128 + cursorPos * 26)

    for i in range(FADE_TIME - 1, -1, -1):
        draw()
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 / FADE_TIME), True)
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)

    u = 0 # gay unpress hack

    while result == None:
        draw()
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)

        if controls.up() and cursorPos > 0:
            if not u:
                cursorPos -= 1
                u = 1
        elif controls.down() and cursorPos < 2:
            if not u:
                cursorPos += 1
                u = 1
        elif controls.attack():
            result = cursorPos
        else:
            u = 0

    # one last draw.  Later on, there's a blurfade that can take advantage of this:
    draw()
    snow.draw()
    return result

    for i in range(FADE_TIME):
        draw()
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, i * 255 / FADE_TIME), True)
        snow.update()
        snow.draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)
