import ika
import snow

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')
    engineRef.mapThings.append(snow.Snow(velocity=(0, 0.5)))

def to2(engineRef):
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 7 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map02.ika-map', (x, 1 * 16))

def to7(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 21 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map07.ika-map', (1 * 16, y))

def to8(engineRef):
    offset_from = 3 * 16  # first vertical pos possible
    offset_to = 29 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map08.ika-map', (48 * 16, y))
