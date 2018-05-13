import ika

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

def to4(engineRef):
    offset_from = 8 * 16  # first horizontal pos possible
    offset_to = 11 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map04.ika-map', (x, 38 * 16))

def to13(engineRef):
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 49 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map13.ika-map', (x, 1 * 16))
