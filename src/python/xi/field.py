# Field (map) handling utility functions
# Coded by Andy Friesen
# 2 November 2003
import ika
import effects

player = None

def spawnPlayer(spriteName, x, y, layerNum = None):
    global player

    if layerNum is None:
        l = ika.Map.GetMetaData().get('entitylayer', 0)
    else:
        l = layerNum

    l = ika.Map.FindLayerByName(l)

    if player is None:
        player = ika.Entity(x, y, l, spriteName)
    else:
        player.x = x
        player.y = y
        if layerNum is not None:
            player.layer = l

    ika.SetPlayer(player)

def mapSwitch(mapName, x, y, layerNum = None, fadeOut = False, fadeIn = False, fade = False):
    if fade or fadeOut:
        effects.fadeOut(50)

    ika.Map.Switch(mapName)
    if player is not None:
        player.x = x
        player.y = y

        if layerNum is None:
            player.layer = ika.Map.GetMetaData().get('entitylayer', 0)
        else:
            player.layer = layerNum

    if fade or fadeIn:
        effects.fadeIn(50)

def warp(x, y, layerNum = None, fadeOut = False, fadeIn = False, fade = False):
    if fade or fadeOut:
        effects.fadeOut(50)

    player.x = x
    player.y = y
    if layerNum is not None:
        player.layer = layerNum

    if fade or fadeIn:
        effects.fadeIn(50)

