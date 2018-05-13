import cabin

def to23(engineRef):
    yield from engineRef.mapSwitchTask('map23.ika-map', (6 * 16, 42 * 16))

def to26(engineRef):
    offset_from = 50 * 16  # first vertical pos possible
    offset_to = 20 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map26.ika-map', (38 * 16, y))

def to30(engineRef):
    yield from engineRef.mapSwitchTask('map30.ika-map', (9*16, 21*16))
    if 'nearend' not in engineRef.saveFlags:
        yield from cabin.sceneTask(engineRef, 'nearend')
