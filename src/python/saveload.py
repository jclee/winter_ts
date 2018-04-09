"""Save/loadgame semantic poop.
   Binary would be a pain in the ass.  Fuckit.  Cheat all you want,
   see if I care.
"""

import ika
import savedata
from statset import StatSet

class SaveGame(object):
    def __init__(self, fileName = None):
        self.stats = StatSet()
        self.flags = {}
        self.mapName = ''
        self.pos = (0, 0, 0)
        if fileName:
            self.load(fileName)

    def getStats(self, engineRef):
        self.stats = engineRef.player.stats.clone()

    def getFlags(self):
        self.flags = {}
        for k, v in savedata.__dict__.items():
            if isinstance(v, (int, str, list, tuple)):
                self.flags[k] = v

    def setStats(self, engineRef):
        engineRef.player.stats = self.stats.clone()

    def setFlags(self):
        self.clearSaveFlags()
        for k, v in self.flags.items():
            savedata.__dict__[k] = v

    def clearSaveFlags():
        destroy = []
        for var, val in savedata.__dict__.items():
            if not var.startswith('_') and isinstance(val, (str, int, list, tuple)):
                destroy.append(var)
        for d in destroy:
            del savedata.__dict__[d]

    clearSaveFlags = staticmethod(clearSaveFlags)

    def currentGame(engineRef):
        s = SaveGame()
        s.getStats(engineRef)
        s.getFlags()
        s.mapName = engineRef.mapName
        p = engineRef.player
        s.pos = (p.x, p.y, p.layer)
        return s

    currentGame = staticmethod(currentGame)

    def setCurrent(self, engineRef):
        self.setStats(engineRef)
        self.setFlags(engineRef)

    def save(self, fileName):
        ika.SetLocalStorageItem(fileName, str(self))

    def load(self, fileName):
        data = ika.GetLocalStorageItem(fileName)
        if data is None:
            raise IOError("file not found")
        self.read(data)

    def __str__(self):
        s = ''
        for k in StatSet.STAT_NAMES:
            s += '%s=%i\n' % (k, self.stats[k])

        s += 'FLAGS\n'
        s += 'MAPNAME=\'%s\'\n' % self.mapName
        s += 'POS=\'%s\'\n' % ','.join([str(x) for x in self.pos])
        for var, val in savedata.__dict__.items():
            if not var.startswith('_'):
                if isinstance(val, (int, str)):
                    s += '%s=%r\n' % (var, val)

                elif isinstance(val, (list, tuple)):
                    s += '%s=LIST\n' % var
                    for el in val:
                        s += '  %s\n' % repr(el)
                    s += 'END\n'
        return s

    def read(self, data):
        lines = [x.strip() for x in data.splitlines()]

        def parse(v):
            v = v.strip()
            if v == 'LIST':
                l = []
                while True:
                    v = lines.pop(0)
                    if v == 'END':      break
                    else:               l.append(parse(v))
                return l

            elif v.startswith("'"):
                return v[1:-1]
            else:
                return int(v)

        # Read stats
        while True:
            s = lines.pop(0)

            if s == 'FLAGS':    break

            p = s.find('=')
            k, v = s[:p], s[p + 1:]
            setattr(self.stats, k, parse(v))

        # read flags
        while lines:
            s = lines.pop(0)
            p = s.find('=')
            k, v = s[:p], parse(s[p + 1:])
            if k == 'MAPNAME':  self.mapName = v
            elif k == 'POS':
                self.pos = tuple([int(x) for x in v.split(',')])
            else:
                self.flags[k] = v
