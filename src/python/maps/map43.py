def to2(engineRef):
    yield from engineRef.mapSwitchTask('map02.ika-map', (48 * 16, engineRef.player.y))

def to44(engineRef):
    offset_from = 3 * 16  # first horizontal pos possible
    offset_to = 22 * 16  # first horizontal pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map44.ika-map', (1 * 16, y))
