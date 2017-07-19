#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class Proxy(object):

    def __init__(self, subject):
        self.__dict__['__subject__'] = subject

    def __getattr__(self, name):
        try:
            return getattr(self.__dict__['__subject__'], name)
        except:
            return object.__getattr__(name)

# end #########################################################################
