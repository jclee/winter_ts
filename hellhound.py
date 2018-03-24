from razormane import RazorMane


class HellHound(RazorMane):

    def __init__(self, *args):
        super(HellHound, self).__init__(*args)
        self.speed = 180
        self.stats.maxhp = 300
        self.stats.hp = 300
        self.stats.att = 33
        self.stats.exp = 80
