#
# Copyright Applied Language Solutions 2012
#
# This file is part of Pypeline.
#
# Pypeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pypeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pypeline.  If not, see <http://www.gnu.org/licenses/>.
#
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

    # return
    # return :: a -> m a
    def return_(self, a):
        return return_(a)

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
