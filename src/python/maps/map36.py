import ika
import snow

def AutoExec(engineRef):
    engineRef.mapThings.append(snow.Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    engineRef.background = ika.Image('gfx/mountains.png')

def to35(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = engineRef.player.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map35.ika-map', (x, 1 * 16))

def to37(engineRef):
    yield from engineRef.mapSwitchTask('map37.ika-map', (engineRef.player.x, 13 * 16))

