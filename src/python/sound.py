import ika
from thing import Thing

class NullSound(object):
    def __init__(self):
        self.position = 0
        self.volume = 1.0

    def Play(self):
        pass

    def Pause(self):
        pass

class RepeatableSound(object):
    def __init__(self, fname):
        self.fname = fname
        self.sounds = [ika.Sound(fname)]
        self.sounds[0].loop = False

    def Play(self):
        for s in self.sounds:
            if s.position == 0:
                s.Play()
                return

        s = ika.Sound(self.fname)
        s.loop = False
        s.Play()
        self.sounds.append(s)

# effects:

slash1, slash2, slash3 = [
    RepeatableSound('sfx/swing%i.wav' % i) for i in range(1,4)
    ]
playerHurt = NullSound()

achievement = RepeatableSound('sfx/LevelUp.wav')

menuClick = RepeatableSound('sfx/MenuClick.wav')
menuBuzz = RepeatableSound('sfx/MenuBuzz.wav')

hearthRend = RepeatableSound('sfx/HearthRend.wav')
crushingGale = RepeatableSound('sfx/CrushingGale.wav')
healingRain = RepeatableSound('sfx/HealingRain.wav')

monsterHit = RepeatableSound('sfx/MonsterHit.wav')

anklebiterStrike = ika.Sound('sfx/AnklebiterStrike.wav')
anklebiterHurt = NullSound() # ika.Sound('sfx/AnklebiterHurt.wav')
anklebiterDie = RepeatableSound('sfx/AnklebiterDie.wav')

yetiStrike = [NullSound(), NullSound()]
yetiHurt = [[ika.Sound('sfx/YetiHurt%i.wav' % i) for i in range(1,4)],
            [ika.Sound('sfx/SoulReaverHurt%i.wav' % i) for i in range(1,4)]]
yetiDie = [ika.Sound('sfx/YetiDie.wav'), ika.Sound('sfx/SoulReaverDie.wav')]

razorManeStrike = RepeatableSound('sfx/RazormaneStrike.wav')
razorManeHurt = RepeatableSound('sfx/RazormaneHurt.wav')
razorManeDie = RepeatableSound('sfx/RazormaneDie.wav')

# other effects?

class Crossfader(Thing):
    def __init__(self):
        self.oldMusic = []
        self._music = None
        self.inc = 0.01

    def _setMusic(self, value):
        assert value is not None
        self._music = value

    music = property(lambda self: self._music, _setMusic)

    def reset(self, newMusic):
        if newMusic is self.music:
            return

        if newMusic in self.oldMusic:
            self.oldMusic.remove(newMusic)

        if self.music is not None:
            if self.music not in self.oldMusic:
                self.oldMusic.append(self.music)

            self.music = newMusic
            self.music.volume = 0.0
            self.music.Play()
        else:
            self.music = newMusic
            self.music.volume = 1.0
            self.music.Play()

    def kill(self):
        if self.music:
            self.music.volume = 0.0
            self.music.Pause()
            self._music = None
            for m in self.oldMusic:
                m.volume = 0
            self.oldMusic = []

    def update(self):
        i = 0
        while i < len(self.oldMusic):
            m = self.oldMusic[i]
            m.volume -= self.inc
            if m.volume <= 0:
                m.Pause()
                self.oldMusic.pop(i)
            else:
                i += 1

        self.music.volume += self.inc

        if not self.oldMusic and self.music.volume >= 1.0:
            return True

    def draw(self):
        pass
