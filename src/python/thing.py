
class Thing(object):
    """As general as you can get.
       Things just hang out onscreen.  HUD elements should be implemented as
       Things, for instance.
    """

    def update(self):
        """Return True to commit suicide here."""
        pass

    def draw(self, *args):
        # requiring that this method be overridden is evil and unpythonic, nazi
        pass
