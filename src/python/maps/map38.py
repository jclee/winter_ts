from browser import window
import ika

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to34(engineRef):
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map34.ika-map', (1 * 16, y))

def to39(engineRef):
    offset_from = 6 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map39.ika-map', (x, 1 * 16))
