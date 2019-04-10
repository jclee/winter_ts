def to46(engineRef):
    yield from engineRef.mapSwitchTask('map46.ika-map', (25 * 16, 13.5 * 16))

def to48(engineRef):
    offset_from = 81 * 16  # first horizontal pos possible
    offset_to = 18 * 16  # first horizontal pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map48.ika-map', (x, 28 * 16))

def to49(engineRef):
    y = engineRef.player.sprite.y
    yield from engineRef.mapSwitchTask('map49.ika-map', (43 * 16, y))
