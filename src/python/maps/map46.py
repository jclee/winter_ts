def to44(engineRef):
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 32 * 16  # first horizontal pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map44.ika-map', (63 * 16, y))

def to47(engineRef):
    yield from engineRef.mapSwitchTask('map47.ika-map', (38 * 16, 3.5 * 16))
