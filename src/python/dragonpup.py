from razormane import RazorMane


class DragonPup(RazorMane):

    def __init__(self, *args):
        super(DragonPup, self).__init__(*args)
        self.sprite.speed = 160
        self.stats.maxhp = 160
        self.stats.hp = 160
        self.stats.att = 28
        self.stats.exp = 34
