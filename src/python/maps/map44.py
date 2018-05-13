def to43(engineRef):
    offset_from = 22 * 16  # first horizontal pos possible
    offset_to = 3 * 16  # first horizontal pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map43.ika-map', (58 * 16, y))

def to45(engineRef):
    offset_from = 28 * 16  # first horizontal pos possible
    offset_to = 23 * 16  # first horizontal pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map45.ika-map', (x, 1 * 16))

def to46(engineRef):
    offset_from = 32 * 16  # first horizontal pos possible
    offset_to = 6 * 16  # first horizontal pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map46.ika-map', (1 * 16, y))

