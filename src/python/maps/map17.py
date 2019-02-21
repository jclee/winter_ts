import ika

def AutoExec(engineRef):
    engineRef.background = engineRef.getImage('gfx/mountains.png')
    ika.Map.SetObs(10,3,3,0)

def to16(engineRef):
    yield from engineRef.mapSwitchTask('map16.ika-map', (38 * 16, engineRef.player.y))

def Tunnel1_1(engineRef):
    ika.Map.SetObs(10,3,3,1)
    ika.Map.SetObs(16,7,3,0)
    ika.Map.SetObs(6,14,3,0)
    yield from engineRef.warpTask((16 * 16, 7 * 16))

def Tunnel1_2(engineRef):
    ika.Map.SetObs(10,3,3,0)
    ika.Map.SetObs(16,7,3,1)
    yield from engineRef.warpTask((10 * 16, 3 * 16))

def Tunnel2_1(engineRef):
    ika.Map.SetObs(6,14,3,1)
    ika.Map.SetObs(15,18,3,0)
    yield from engineRef.warpTask((15 * 16, 18 * 16))

def Tunnel2_2(engineRef):
    ika.Map.SetObs(6,14,3,0)
    ika.Map.SetObs(15,18,3,1)
    yield from engineRef.warpTask((6 * 16, 14 * 16))

def Around1(engineRef):
    yield from engineRef.warpTask((1.5 * 16, 15 * 16))

def Around2(engineRef):
    yield from engineRef.warpTask((18.5 * 16, 18 * 16))
