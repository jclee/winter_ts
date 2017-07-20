#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# modules #####################################################################

class Null:

    def __abs__(self):
        return 0

    def __add__(self, other):
        return other

    def __and__(self, other):
        return other

    def __call__(self, *args, **kwargs):
        return self

    def __coerce__(self, other):
        return None

    def __complex__(self):
        return 0j

    def __contains__(self, item):
        return False

    def __delattr__(self, key):
        return self

    def __delitem__(self, key):
        return self

    def __div__(self, other):
        return other

    def __divmod__(self, other):
        return other

    def __eq__(self, other):
        return False

    def __float__(self):
        return .0

    def __floordiv__(self, other):
        return other

    def __ge__(self, other):
        return False

    def __getattr__(self, key):
        return self

    def __getitem__(self, key):
        return self

    def __gt__(self, other):
        return False

    def __hash__(self):
        return 0

    def __hex__(self):
        return 0

    def __iadd__(self, other):
        return other

    def __iand__(self, other):
        return other

    def __idiv__(self, other):
        return other

    def __ifloordiv__(self, other):
        return other

    def __ilshift__(self, other):
        return other

    def __imod__(self, other):
        return other

    def __imul__(self, other):
        return other

    def __init__(self, *args, **kwargs):
        return None

    def __int__(self):
        return 0

    def __invert__(self):
        return 0

    def __ior__(self, other):
        return other

    def __ipow__(self, other, modulo=None):
        return self

    def __irshift__(self, other):
        return other

    def __isub__(self, other):
        return other

    def __iter__(self):
        return iter(())

    def __itruediv__(self, other):
        return other

    def __ixor__(self, other):
        return other

    def __le__(self, other):
        return False

    def __len__(self):
        return 0

    def __long__(self):
        return 0

    def __lshift__(self, other):
        return other

    def __lt__(self, other):
        return False

    def __mod__(self, other):
        return other

    def __mul__(self, other):
        return other

    def __ne__(self, other):
        return False

    def __neg__(self):
        return 0

    def __nonzero__(self):
        return False

    def __oct__(self):
        return 0

    def __or__(self, other):
        return other

    def __pos__(self):
        return 0

    def __pow__(self, other, modulo=None):
        return self

    def __radd__(self, other):
        return other

    def __rand__(self, other):
        return other

    def __rdiv__(self, other):
        return other

    def __rdivmod__(self, other):
        return other

    def __repr__(self):
        return '<Null>'

    def __rfloordiv__(self, other):
        return other

    def __rlshift__(self, other):
        return other

    def __rmod__(self, other):
        return other

    def __rmul__(self, other):
        return other

    def __ror__(self, other):
        return other

    def __rpow__(self, other):
        return other

    def __rrshift__(self, other):
        return other

    def __rshift__(self, other):
        return other

    def __rsub__(self, other):
        return other

    def __rtruediv__(self, other):
        return other

    def __rxor__(self, other):
        return other

    def __setattr__(self, key, value):
        return self

    def __setitem__(self, key, value):
        return self

    def __str__(self):
        return 'Null'

    def __sub__(self, other):
        return other

    def __truediv__(self, other):
        return other

    def __xor__(self, other):
        return other


Null = Null()

# end #########################################################################
