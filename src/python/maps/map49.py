def to1(engineRef):
    yield from engineRef.mapSwitchTask('map01.ika-map', (53 * 16, 4.5 * 16))

def to47(engineRef):
    y = engineRef.player.y
    yield from engineRef.mapSwitchTask('map47.ika-map', (1 * 16, y))
