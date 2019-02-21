import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to21(engineRef):
    yield from engineRef.mapSwitchTask('map21.ika-map', (38 * 16, engineRef.player.y))

def to50(engineRef):
    yield from engineRef.mapSwitchTask('map50.ika-map', (9 * 16, 13 * 16))
