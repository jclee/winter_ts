import ika

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

def to16(engineRef):
    offset_from = 44 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map16.ika-map', (1 * 16, y))

def to21(engineRef):
    yield from engineRef.mapSwitchTask('map21.ika-map', (engineRef.player.x, 38 * 16))
