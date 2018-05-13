
class StatSet(object):

    STAT_NAMES = (
        '_hp', '_mp', 'maxhp', 'maxmp',
        'att', 'mag', 'pres', 'mres',
        'level', 'exp', 'next',
        )

    def __init__(self, **kw):
        for name in self.STAT_NAMES:
            setattr(self, name, kw.get(name, 0))
        # special hack:
        if 'hp' in kw:
            self.hp = kw['hp']
        if 'mp' in kw:
            self.mp = kw['mp']

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise KeyError, key

    hp = property(lambda self: self._hp, lambda self, value: setattr(self, '_hp', max(0, min(self.maxhp, value))))
    mp = property(lambda self: self._mp, lambda self, value: setattr(self, '_mp', max(0, min(self.maxmp, value))))

    def clone(self):
        s = StatSet()
        for name in self.STAT_NAMES:
            setattr(s, name, getattr(self, name))
        return s
