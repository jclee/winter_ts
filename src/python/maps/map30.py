def to25(engineRef):
    yield from engineRef.mapSwitchTask('map25.ika-map', (39 * 16, 5 * 16))

def to31(engineRef):
    x = engineRef.player.x + 16
    yield from engineRef.mapSwitchTask('map31.ika-map', (x, 28 * 16))
