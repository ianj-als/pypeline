import types

from pypeline.core.types.monad import Maybe


#
# Just a value
#
class Just(Maybe):
    def __init__(self, a):
        if a is None:
            raise ValueError("Value cannot be None")
        self._a = a

    def __ge__(self, function):
        if type(function) is not types.FunctionType and \
           type(function) is not types.MethodType:
            raise ValueError("Must be a function or method")
        result = function(self._a)
        return result

    def __eq__(self, other):
        if not isinstance(other, Just):
            return False
        if other is None:
            return False
        if self._a == other._a:
            return True
        return False

    def __hash__(self):
        return self._a.__hash__()

    def __repr__(self):
        return "<Just %s>" % str(self._a)

    def __nonzero__(self):
        return True


def return_(a):
    return Just(a)
