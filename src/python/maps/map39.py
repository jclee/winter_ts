from browser import window
import ika

def AutoExec(engineRef):
    engineRef.mapThings.append(window.Snow.new(engineRef, 600, [.4, 1], [192,192,255]))
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to38(engineRef):
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map38.ika-map', (x, 28 * 16))

def to40(engineRef):
    offset_from = 5 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    x = engineRef.player.sprite.x - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map40.ika-map', (x, 1 * 16))

def to41(engineRef):
    offset_from = 34 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = engineRef.player.sprite.y - offset_from + offset_to
    yield from engineRef.mapSwitchTask('map41.ika-map', (1 * 16, y))
