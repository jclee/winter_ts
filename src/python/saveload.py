"""Save/loadgame semantic poop.
   Binary would be a pain in the ass.  Fuckit.  Cheat all you want,
   see if I care.
"""

import savedata
import system
from statset import StatSet

class SaveGame(object):
    def __init__(self, fileName = None):
        self.stats = StatSet()
        self.flags = {}
        self.mapName = ''
        self.pos = (0, 0, 0)
        if fileName:
            self.load(fileName)

    def getStats(self):
        self.stats = system.engine.player.stats.clone()

    def getFlags(self):
        self.flags = {}
        for k, v in savedata.__dict__.iteritems():
            if isinstance(v, (int, str, list, tuple)):
                self.flags[k] = v

    def setStats(self):
        system.engine.player.stats = self.stats.clone()

    def setFlags(self):
        self.clearSaveFlags()
        for k, v in self.flags.iteritems():
            savedata.__dict__[k] = v

    def clearSaveFlags():
        destroy = []
        for var, val in savedata.__dict__.iteritems():
            if not var.startswith('_') and isinstance(val, (str, int, list, tuple)):
                destroy.append(var)
        for d in destroy:
            del savedata.__dict__[d]

    clearSaveFlags = staticmethod(clearSaveFlags)

    def currentGame():
        s = SaveGame()
        s.getStats()
        s.getFlags()
        s.mapName = system.engine.mapName
        p = system.engine.player
        s.pos = (p.x, p.y, p.layer)
        return s

    currentGame = staticmethod(currentGame)

    def setCurrent(self):
        self.setStats()
        self.setFlags()

    def save(self, fileName):
        file(fileName, 'wt').write(str(self))

    def load(self, fileName):
        self.read(file(fileName, 'rt'))

    def __str__(self):
        s = ''
        for k in StatSet.STAT_NAMES:
            s += '%s=%i\n' % (k, self.stats[k])

        s += 'FLAGS\n'
        s += 'MAPNAME=\'%s\'\n' % self.mapName
        s += 'POS=\'%s\'\n' % ','.join([str(x) for x in self.pos])
        for var, val in savedata.__dict__.iteritems():
            if not var.startswith('_'):
                if isinstance(val, (int, str)):
                    s += '%s=%r\n' % (var, val)

                elif isinstance(val, (list, tuple)):
                    s += '%s=LIST\n' % var
                    for el in val:
                        s += '  %s\n' % `el`
                    s += 'END\n'
        return s

    def read(self, f):
        lines = [x.strip() for x in f.readlines()]

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
            else:               self.flags[k] = v

def test():
    savedata.test1 = 'COCKS'
    savedata.test8 = 1337
    savedata.test1337 = range(10,40)
    sg = SaveGame.currentGame()
    #sg.save('bleh.txt')
    #f = file('bleh.txt', 'w')
    #writeSaveFlags(f)
    #f.close()

    #f = file('bleh.txt', 'r')
    #readSaveFlags(f)
    #f.close()
    bleh = SaveGame()
    bleh.load('bleh.txt')
    bleh.setCurrent()
    s = StatSet.STAT_NAMES

    print(`savedata.test1`)
    print(`savedata.test8`)
    print(`savedata.test1337`)

#test()
