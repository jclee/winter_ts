import cabin

def to30(engineRef):
    x = engineRef.player.x - 160
    yield from engineRef.mapSwitchTask('map30.ika-map', (6 * 16 + x, 16))
    if 'nearend' not in engineRef.saveFlags:
        yield from cabin.sceneTask(engineRef, 'nearend')

def to32(engineRef):
    # no adjustment here on purpose
    yield from engineRef.mapSwitchTask('map32.ika-map', (25 * 16, 38 * 16))
