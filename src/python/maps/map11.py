import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to8(engineRef):
    offset_from = 21 * 16  # first horizontal pos possible
    offset_to = 23 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map08.ika-map', (x, 38 * 16))

def to12(engineRef):
    yield from engineRef.mapSwitchTask('map12.ika-map', (10 * 16, 18 * 16))
