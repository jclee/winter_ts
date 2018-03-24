
# Implementation of the Proxy design pattern

class Proxy(object):
    def __init__(self, subject):
        self.__subject = subject

    def getSubject(self):
        return self.__subject

    def __setattr__(self, name, value):
        # hack
        if name.endswith('__subject'):
            return object.__setattr__(self, name, value)
        else:
            return setattr(self.__subject, name, value)
        
    def __getattr__(self, name):
        return getattr(self.__subject, name)