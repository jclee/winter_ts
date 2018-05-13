def to47(engineRef):
    offset_from = 18 * 16  # first horizontal pos possible
    offset_to = 81 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map47.ika-map', (x, 1 * 16))
