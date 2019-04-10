from browser import window
import ika

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to39(engineRef):
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 34 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map39.ika-map', (38 * 16, y))

def to42(engineRef):
    yield from engineRef.mapSwitchTask('map42.ika-map', (engineRef.player.sprite.x - 16, 1 * 16))
