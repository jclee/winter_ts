def to27(engineRef):
    offset_from = 13 * 16  # first vertical pos possible
    offset_to = 33 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map27.ika-map', (x, 1 * 16))
