from browser import window

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')
    engineRef.mapThings.append(window.Snow.new(engineRef))

def to6(engineRef):
    offset_from = 21 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map06.ika-map', (38 * 16, y))

def to13(engineRef):
    yield from engineRef.mapSwitchTask('map13.ika-map', (1 * 16, engineRef.player.sprite.y))
