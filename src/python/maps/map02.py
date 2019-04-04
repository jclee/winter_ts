from browser import window

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 3000, [-1, 1.5]))

def to1(engineRef):
    offset_from = 38 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map01.ika-map', (1 * 16, y))

def to3(engineRef):
    offset_from = 14 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map03.ika-map', (98 * 16, y))

def to6(engineRef):
    offset_from = 7 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map06.ika-map', (x, 38 * 16))

def to43(engineRef):
    yield from engineRef.mapSwitchTask('map43.ika-map', (1 * 16, engineRef.player.y))
