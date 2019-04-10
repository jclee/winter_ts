from browser import window

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 4000, [-1, 1.5]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to7(engineRef):
    yield from engineRef.mapSwitchTask('map07.ika-map', (78 * 16, engineRef.player.sprite.y))

def to14(engineRef):
    offset_from = 49 * 16  # first horizontal pos possible
    offset_to = 6 * 16  # first horizontal pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map14.ika-map', (x, 28 * 16))

def to16(engineRef):
    yield from engineRef.mapSwitchTask('map16.ika-map', (1 * 16, engineRef.player.sprite.y))
