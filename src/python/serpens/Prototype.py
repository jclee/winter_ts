#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# modules #####################################################################

from copy import deepcopy

# main ########################################################################

class Prototype:

    def __init__(self):
        self.__objdict = {}

    def register(self, name, obj):
        self.__objdict[name] = obj

    def unregister(self, name):
        del self.__objdict[name]

    def clone(self, name, **new):
        obj = deepcopy(self.__objdict[name])
        obj.__dict__.update(new)
        return obj

# end #########################################################################
