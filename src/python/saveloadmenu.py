# Stand-in load/save menu code

import ika
from browser import window

def loadMenuTask(engineRef, resultRef, fadeOut=True):
    title = window.gui.TextFrame.new(engineRef, ['Load Game'])
    title.setPosition((16, 16))
    saves = engineRef.readSaves()
    m = window.gui.SaveLoadMenu.new(engineRef, saves, False)

    def draw():
        engineRef.video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from ika.asTask(window.effects.fadeInTask(engineRef, 50, draw))

    i = None
    while i is None:
        i = m.update()
        draw()
        engineRef.video.ShowPage()
        yield None

    if fadeOut:
        yield from ika.asTask(window.effects.fadeOutTask(engineRef, 50, draw))

    draw()
    # Hack to get around brython's lack of support for returning values through
    # "yield from":
    if i == 'cancel' or i >= len(saves):
        resultRef[0] = None
    else:
        resultRef[0] = saves[i]

def saveMenuTask(engineRef):
    title = window.gui.TextFrame.new(engineRef, ['Save Game'])
    title.setPosition((16, 16))
    saves = engineRef.readSaves()
    m = window.gui.SaveLoadMenu.new(engineRef, saves, True)

    def draw():
        engineRef.video.ClearScreen() # fix this
        m.draw()
        title.draw()

    yield from ika.asTask(window.effects.fadeInTask(engineRef, 50, draw))

    i = None
    while i is None:
        i = m.update()
        draw()
        engineRef.video.ShowPage()
        yield None

    if i != 'cancel':
        engineRef.writeSave(i)

    yield from ika.asTask(window.effects.fadeOutTask(engineRef, 50, draw))
