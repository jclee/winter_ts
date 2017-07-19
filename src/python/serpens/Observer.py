#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class Subject:

    def __init__(self):
        super(Subject, self).__init__()
        self.__observers = []

    def attach(self, observer):
        self.__observers.append(observer)
        return self

    def detach(self, observer):
        try:
            self.__observers.remove(observer)
        except:
            pass
        return self

    def notify(self):
        for observer in self.__observers:
            observer.update(self)
        return self


class Observer(object):
    pass

# end #########################################################################
