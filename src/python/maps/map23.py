import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')

def to21(engineRef):
    yield from engineRef.mapSwitchTask('map21.ika-map', (1 * 16, engineRef.player.y))

def to24(engineRef):
    yield from engineRef.mapSwitchTask('map24.ika-map', (48 * 16, 34 * 16))

def to25(engineRef):
    yield from engineRef.mapSwitchTask('map25.ika-map', (54 * 16, 55 * 16))

def Tunnel1_1(engineRef):
    yield from engineRef.warpTask((21 * 16, 21 * 16))

def Tunnel1_2(engineRef):
    yield from engineRef.warpTask((31 * 16, 36 * 16))

def Tunnel2_1(engineRef):
    if False:
        yield None

def Tunnel2_2(engineRef):
    if False:
        yield None

def Tunnel3_1(engineRef):
    yield from engineRef.warpTask((6 * 16, 16 * 16))

def Tunnel3_2(engineRef):
    yield from engineRef.warpTask((22 * 16, 27 * 16))

def Tunnel4_1(engineRef):
    yield from engineRef.warpTask((5 * 16, 34 * 16))

def Tunnel4_2(engineRef):
    yield from engineRef.warpTask((30 * 16, 8 * 16))

def Tunnel5_1(engineRef):
    yield from engineRef.warpTask((18 * 16, 36 * 16))

def Tunnel5_2(engineRef):
    yield from engineRef.warpTask((45 * 16, 44 * 16))

def Tunnel6_1(engineRef):
    yield from engineRef.warpTask((45 * 16, 37 * 16))

def Tunnel6_2(engineRef):
    yield from engineRef.warpTask((6 * 16, 25 * 16))

def Tunnel7_1(engineRef):
    if False:
        yield None

def Tunnel7_2(engineRef):
    if False:
        yield None
