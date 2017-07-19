#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# main ########################################################################

class AbstractFactory(object):

    def __init__(self):
        super(AbstractFactory, self).__init__()
        self.__products = {}

    def register(self, name, product):
        self.__products[name] = product

    def unregister(self, name):
        del self.__products[name]

    def create(self, name):
        return self.__products[name]()

# end #########################################################################
