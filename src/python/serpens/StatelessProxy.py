#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class StatelessProxy(object):

    def __init__(self):
        super(StatelessProxy, self).__init__()
        if '__shared__' not in self.__class__.__dict__:
            self.__class__.__shared__ = {}
        self.__dict__ = self.__class__.__shared__

# end #########################################################################
