#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class PolicyClass(type):                      # All metaclasses inherit type.
    __dict = {}                               # Used to store created classes.
    def __new__(cls, name, bases, d):         # class, name, bases, dict
        def __make(*T):                       # Wrapper function for old class.
            try:                              #     T* = Bases of new class.
                this = cls.__dict[(name, T)]  # Make the class doesn't already
            except KeyError:                  #     exist.
                L = [C for C in (bases + T)   # Add policies to original bases.
                    if C is not type]         # Remove <type> from bases.
                L.sort(lambda x, y:           #
                    cmp(id(x), id(y)))        #
                this = type(name,             # Construct new class using type.
                    tuple(L), d)              # type() only accepts tuples.
                cls.__dict[(name, T)] = this  # Store new class for later use.
            return this                       # Return resulting class.
        return __make                         # Replace original class.

# end #########################################################################
