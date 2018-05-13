def to8(engineRef):
    yield from engineRef.mapSwitchTask('map08.ika-map', (engineRef.player.x, 1 * 16))

def to41(engineRef):
    yield from engineRef.mapSwitchTask('map41.ika-map', (engineRef.player.x + 16, 38 * 16))
