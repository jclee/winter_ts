import ika
import snow

def AutoExec(engineRef):
    engineRef.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to34(engineRef):
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = engineRef.player.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map34.ika-map', (1 * 16, y))

def to39(engineRef):
    offset_from = 6 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map39.ika-map', (x, 1 * 16))
