import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to34(engineRef):
    offset_from = 11 * 16  # first vertical pos possible
    offset_to = 42 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map34.ika-map', (x, 1 * 16))

def to36(engineRef):
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map36.ika-map', (x, 38 * 16))
