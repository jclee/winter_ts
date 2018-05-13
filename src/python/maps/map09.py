def to8(engineRef):
    yield from engineRef.mapSwitchTask('map08.ika-map', (1 * 16, engineRef.player.y))

def to10(engineRef):
    yield from engineRef.mapSwitchTask('map10.ika-map', (engineRef.player.x, 28 * 16))
