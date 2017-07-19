#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# modules #####################################################################

from AbstractFactory import *
from AutoProperty import *
from ChildList import *
from ClassPolicies import *
from Null import *
from Observer import *
#from Prototype import *
from Proxy import *
from Singleton import *
from StatelessProxy import *
from StateMachine import *
#from WeakMethod import *

def issequence(obj):
    return hasattr(obj, '__getitem__')

def isgenerator(obj):
    return hasattr(obj, 'gi_frame')

def dictinvert(D):
    return dict(zip(D.values(), D.keys()))

def dictmap(function, D):
    return dict(map(function, D.items()))

def dictfilter(function, D):
    return dict(filter(function, D.items()))

def dictreduce(function, D):
    return dict(reduce(function, D.items()))

def intersect(a, b):
    [i for i in a if a in b]

# end #########################################################################