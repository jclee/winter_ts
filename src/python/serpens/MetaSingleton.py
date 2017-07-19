#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

def MetaSingleton(name, bases, d):
    return type(name, bases, d)()


def MetaStaticSingleton(name, bases, d):
    for i in d:
        if callable(d[i]):
            d[i] = staticmethod(d[i])
    return type(name, bases, d)()

# end #########################################################################
