import snow

def AutoExec(engineRef):
    engineRef.mapThings.append(snow.Snow(velocity=(0, 0.5)))

def to6(engineRef):
    offset_from = 29 * 16  # first vertical pos possible
    offset_to = 3 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map06.ika-map', (1 * 16, y))

def to9(engineRef):
    yield from engineRef.mapSwitchTask('map09.ika-map', (28 * 16, engineRef.player.y))

def to11(engineRef):
    offset_from = 23 * 16  # first vertical pos possible
    offset_to = 21 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map11.ika-map', (x, 1 * 16))

def to42(engineRef):
    yield from engineRef.mapSwitchTask('map42.ika-map', (engineRef.player.x, 28 * 16))
