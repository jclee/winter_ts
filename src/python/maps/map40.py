import ika

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

def to39(engineRef):
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 5 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map39.ika-map', (x, 38 * 16))
