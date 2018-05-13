"""Save/loadgame semantic poop.
   Binary would be a pain in the ass.  Fuckit.  Cheat all you want,
   see if I care.
"""

from statset import StatSet

class SaveGame(object):
    def __init__(self, engineRef, fileName = None):
        self.stats = StatSet()
        self.flags = {}
        self.mapName = ''
        self.pos = (0, 0, 0)
        if fileName:
            data = engineRef.getLocalStorageItem(fileName)
            if data is None:
                raise IOError("file not found")
            self.read(data)

    def getStats(self, engineRef):
        self.stats = engineRef.player.stats.clone()

    def getFlags(self, engineRef):
        self.flags = {}
        for k, v in engineRef.saveFlags.items():
            if isinstance(v, (int, str, list, tuple)):
                self.flags[k] = v

    def setStats(self, engineRef):
        engineRef.player.stats = self.stats.clone()

    def setFlags(self, engineRef):
        engineRef.saveFlags = dict(self.flags)

    def currentGame(engineRef):
        s = SaveGame(engineRef)
        s.getStats(engineRef)
        s.getFlags(engineRef)
        s.mapName = engineRef.mapName
        p = engineRef.player
        s.pos = (p.x, p.y, p.layer)
        return s

    currentGame = staticmethod(currentGame)

    def setCurrent(self, engineRef):
        self.setStats(engineRef)
        self.setFlags(engineRef)

    def save(self, engineRef, fileName):
        engineRef.setLocalStorageItem(fileName, self._toStringData(engineRef))

    def _toStringData(self, engineRef):
        s = ''
        s += '_hp=%i\n' % self.stats._hp
        s += '_mp=%i\n' % self.stats._mp
        s += 'att=%i\n' % self.stats.att
        s += 'exp=%i\n' % self.stats.exp
        s += 'level=%i\n' % self.stats.level
        s += 'mag=%i\n' % self.stats.mag
        s += 'maxhp=%i\n' % self.stats.maxhp
        s += 'maxmp=%i\n' % self.stats.maxmp
        s += 'mres=%i\n' % self.stats.mres
        s += 'next=%i\n' % self.stats.next
        s += 'pres=%i\n' % self.stats.pres

        s += 'FLAGS\n'
        s += 'MAPNAME=\'%s\'\n' % self.mapName
        s += 'POS=\'%s\'\n' % ','.join([str(x) for x in self.pos])
        for var, val in engineRef.saveFlags.items():
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
