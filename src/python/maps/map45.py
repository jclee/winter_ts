import ika

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')

def to44(engineRef):
    offset_from = 23 * 16  # first horizontal pos possible
    offset_to = 28 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map44.ika-map', (x, 48 * 16)) 
