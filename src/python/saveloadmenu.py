# Stand-in load/save menu code

import controls
import effects
import gui
import ika
from browser import window

def loadMenuTask(engineRef, resultRef, fadeOut=True):
    title = gui.TextFrame.new(engineRef, ['Load Game'])
    title.setPosition((16, 16))
    saves = engineRef.readSaves()
    m = gui.SaveLoadMenu.new(engineRef, saves, False)

    def draw():
        ika.Video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from effects.fadeInTask(50, draw=draw)

    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()
        yield None

    if fadeOut:
        yield from effects.fadeOutTask(50, draw=draw)

    draw()
    # Hack to get around brython's lack of support for returning values through
    # "yield from":
    if i == 'cancel' or i >= len(saves):
        resultRef[0] = None
    else:
        resultRef[0] = saves[i]

def saveMenuTask(engineRef):
    title = gui.TextFrame.new(engineRef, ['Save Game'])
    title.setPosition((16, 16))
    saves = engineRef.readSaves()
    m = gui.SaveLoadMenu.new(engineRef, saves, True)

    def draw():
        ika.Video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from effects.fadeInTask(50, draw=draw)

    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()
        yield None

    if i != 'cancel':
        engineRef.writeSave(i)

    yield from effects.fadeOutTask(50, draw=draw)
