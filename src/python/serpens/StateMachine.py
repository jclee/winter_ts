#!/usr/bin/env python

# author: Ian Douglas Bollinger
# This file has been placed in the public domain.

# exceptions ##################################################################

class StateMachineError(RuntimeError):
    pass

# main ########################################################################

class BasicStateMachine(object):
    
    def __init__(self, initial_state):
        super(BasicStateMachine, self).__init__()
        self._handlers = {}
        self._initial_state = initial_state
        self._current_state = initial_state
        self.__default_state = None

    def addState(self, name, handler):
        self._handlers[name] = handler().next
        return self

    def reset(self):
        self._current_state = self._initial_state
        return self
    
    def _getState(self):
        try:
            return self._handlers[self._current_state]
        except KeyError:
            assert self.__default_state is not None
            return self.__default_state
    
    def run(self):
        self.__curent_state = self._getState()(self)
        return self

    default_state = property(
                        lambda self: self.__default_state,
                        lambda self, v: setattr(self, '__default_state', v),
                        lambda self: setattr(self, '__default_state', None)
                    )


class StateMachine(BasicStateMachine):

    def __init__(self, initial_state):
        super(StateMachine, self).__init__(initial_state)
 
    def addState(self, name, handler, data=None):
        if symbol is None:
            return super(StateMachine, self).addState(name, handler)
        self._states[(name, data)] = handler(data).next
        return self

    def _getState(self, data):
        try:
            return self.__handlers[(self._current_state, symbol)]
        except KeyError:
            super(StateMachine, self)._getState()

    def run(self, data):
        self._current_state = self._getState(data)(self) or self._initial_state

# end #########################################################################
