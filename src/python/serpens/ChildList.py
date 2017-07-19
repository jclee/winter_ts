#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class ChildList(list):

    def __new__(self, bound):
        return list.__new__(self)

    def __init__(self, bound):
        super(ChildList, self).__init__()
        self.__bound = bound

    def __setitem__(self, index, obj):
        obj.parent = self.__bound
        list.__setitem__(self, index, obj)

    def __delitem__(self, index):
        obj.parent = Null
        list.__delitem__(self, index)

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    def insert(self, index, obj):
        obj.parent = self.__bound
        list.insert(self, index, obj)

    def pop(self, index=-1):
        self[index].parent = Null
        return list.pop(self, index)

    def remove(self, obj):
        obj.parent = Null
        list.remove(self, obj)

    def append(self, obj):
        obj.parent = self.__bound
        list.append(self, obj)

# end #########################################################################
