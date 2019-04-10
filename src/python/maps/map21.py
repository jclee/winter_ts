import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to19(engineRef):
    yield from engineRef.mapSwitchTask('map19.ika-map', (engineRef.player.sprite.x, 1 * 16))

def to22(engineRef):
    yield from engineRef.mapSwitchTask('map22.ika-map', (1 * 16, engineRef.player.sprite.y))

def to23(engineRef):
    yield from engineRef.mapSwitchTask('map23.ika-map', (48 * 16, engineRef.player.sprite.y))

def lowerPath(engineRef):
    engineRef.player.sprite.layer = 1
    if False:
        yield None

def middlePath(engineRef):
    engineRef.player.sprite.layer = 3
    if False:
        yield None

def upperPath(engineRef):
    engineRef.player.sprite.layer = 4
    if False:
        yield None
