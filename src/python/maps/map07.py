import ika
import snow

def AutoExec(engineRef):
    engineRef.background = ika.Image('gfx/mountains.png')
    engineRef.mapThings.append(snow.Snow(velocity=(0, 0.5)))

def to6(engineRef):
    offset_from = 21 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map06.ika-map', (38 * 16, y))

def to13(engineRef):
    yield from engineRef.mapSwitchTask('map13.ika-map', (1 * 16, engineRef.player.y))
