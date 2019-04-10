def to26(engineRef):
    yield from engineRef.mapSwitchTask('map26.ika-map', (engineRef.player.sprite.x, 1 * 16))

def to28(engineRef):
    offset_from = 33 * 16  # first vertical pos possible
    offset_to = 13 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map28.ika-map', (x, 28 * 16))

def to29(engineRef):
    offset_from = 22 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map29.ika-map', (1 * 16, y))

def to34(engineRef):
    yield from engineRef.mapSwitchTask('map34.ika-map', (74 * 16, 6.5 * 16))

