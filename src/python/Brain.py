from browser import window
import ika

class Brain(object):
    '''
    The brain is a very high level abstraction over an enemy's behaviour.
    Brains consist of a number of moods, each of which having its
    own desirability factor. (an arbitrary integer)

    A mood is checked every so often.  For now, it's random, weighted
    by desirability.
    '''
    def __init__(self):
        self.moods = []
        self.curMood = None

    def chooseMood(self):
        # weighted random pick:

        N = sum([x.desirability for x in self.moods])
        n = window.random(0, N)

        for p in self.moods:
            if n < p.desirability:
                return p
            else:
                n -= p.desirability

        return None

    def think(self):
        'Using the term liberally. ;)'

        self.curMood = self.chooseMood()
        return self.curMood

# moods follow.
class Mood(object):
    def __init__(self, d):
        self.desirability = d

class Flee(Mood):
    pass

class Attack(Mood):
    pass

class Passive(Mood):
    pass

class Regroup(Mood):
    pass
