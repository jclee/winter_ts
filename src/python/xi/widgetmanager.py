# Widget management class
# This is very general by very nature.  There's not much here, just a collection
# of updatable, drawable things.
# Coded by Andy Friesen
# 2 Nov 2003

import ika

class WidgetManager(object):
    def __init__(self):
        self.children = []

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)

    def update(self, timeDelta):
        for child in self.children:
            try:
                result = child.update(timeDelta)

            except ManagerCommand, cmd:
                cmd(self)

            except (AttributeError, TypeError):      # don't care if there's an update method or not.  Do nothing if it does not exist.
                pass

    def draw(self):
        for child in self.children:
            child.draw()
