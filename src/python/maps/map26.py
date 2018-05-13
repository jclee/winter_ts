def to25(engineRef):
    offset_from = 20 * 16  # first vertical pos possible
    offset_to = 50 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map25.ika-map', (1 * 16, y))

def to27(engineRef):
    yield from engineRef.mapSwitchTask('map27.ika-map', (engineRef.player.x, 78 * 16))
