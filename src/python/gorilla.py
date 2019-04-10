from yeti import Yeti


class Gorilla(Yeti):

    def __init__(self, *args):
        super(Gorilla, self).__init__(*args)
        self.sprite.speed = 90
        self.stats.maxhp = 300
        self.stats.hp = 200
        self.stats.att = 36
        self.stats.exp = 200
