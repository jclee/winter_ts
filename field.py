
class Field(object):
    """A field is just a big invisible thing that does something if the player
       walks on to it.  Warp points can be fields, as can plot-based zone
       thingies.
    """

    def __init__(self, rect, layer, scriptTask):
        self.pos = rect[:2]
        self.size = rect[2:]
        self.layer = layer
        self.scriptTask = scriptTask
        self.rect = rect

    def fireTask(self):
        yield from self.scriptTask()

    def test(self, p):
        if p.layer != self.layer:
            return False

        x, y = self.pos
        w, h = self.size
        if x - p.ent.hotwidth  < p.x < x + w and \
           y - p.ent.hotheight < p.y < y + h:
            return True
        else:
            return False
