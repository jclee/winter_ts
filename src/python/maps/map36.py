from browser import window
import ika

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to35(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map35.ika-map', (x, 1 * 16))

def to37(engineRef):
    yield from engineRef.mapSwitchTask('map37.ika-map', (engineRef.player.sprite.x, 13 * 16))

