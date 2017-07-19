#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class Singleton(type):
    
    def __new__(cls, name, bases, namespace):
        return type(name, bases, namespace)()
    
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class StaticSingleton(Singleton):
    
    def __init__(cls, name, bases, namespace):
        super(StaticSingleton, cls).__init__(name, bases, namespace)
        for key in namespace:
            if callable(namespace[key]):
                namespace[key] = staticmethod(namespace[key])

# end #########################################################################
