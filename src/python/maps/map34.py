import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def manaPool(engineRef):
    engineRef.player.stats.mp += 1
    if False:
        yield None

def to27(engineRef):
    yield from engineRef.mapSwitchTask('map27.ika-map', (6 * 16, 34 * 16))

def to35(engineRef):
    offset_from = 42 * 16  # first vertical pos possible
    offset_to = 11 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map35.ika-map', (x, 23 * 16))

def to38(engineRef):
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map38.ika-map', (28 * 16, y))
