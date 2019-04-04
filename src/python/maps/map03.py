from browser import window

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 5000, [-.5, 2]))

def to2(engineRef):
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 14 * 16  # first horizontal pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map02.ika-map', (1 * 16, y))

def to4(engineRef):
    offset_from = 8 * 16  # first horizontal pos possible
    offset_to = 11 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map04.ika-map', (x, 38 * 16))
