import ika

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

def to19(engineRef):
    yield from engineRef.mapSwitchTask('map19.ika-map', (engineRef.player.x, 1 * 16))

def to22(engineRef):
    yield from engineRef.mapSwitchTask('map22.ika-map', (1 * 16, engineRef.player.y))

def to23(engineRef):
    yield from engineRef.mapSwitchTask('map23.ika-map', (48 * 16, engineRef.player.y))

def lowerPath(engineRef):
    engineRef.player.layer = 1
    if False:
        yield None

def middlePath(engineRef):
    engineRef.player.layer = 3
    if False:
        yield None

def upperPath(engineRef):
    engineRef.player.layer = 4
    if False:
        yield None
