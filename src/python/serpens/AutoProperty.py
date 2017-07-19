#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

def AutoProperty(name, bases, d):
    return property(d.get('__get__'), d.get('__set__'), d.get('__delete__'),
                    d.get('__doc__'))

# end #########################################################################
