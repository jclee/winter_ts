#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# modules #####################################################################

import weakref

# main ########################################################################

class _WeakBoundMethod:

    def __init__(self, f):
        self.f = f.im_func
        self.ref = weakref.ref(f.im_self)

    def __call__(self, *args, **kwargs):
        if self.ref() is None:
            raise TypeError, "Method called on a non-existant object."
        apply(self.f, (self.ref(),) + args, kwargs)


class _WeakMethod:

    def __init__(self, f):
        self.f = weakref.ref(f)

    def __call__(self , *args, **kwargs):
        if self.f() is None:
            raise TypeError, "Function no longer exists."
        apply(self.f(), args)


def WeakMethod(f):
    if _ismethod(f):
        return _WeakBoundMethod(f)
    return _WeakMethod(f)


def _ismethod(f):
    return hasattr(f, 'im_func')

# end #########################################################################
