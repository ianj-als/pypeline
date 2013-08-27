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

from pypeline.core.types.monad import Monad


# Continuation monad
class Cont(Monad):
    def __init__(self, a):
        super(Monad, self).__init__()
        if type(a) is not types.FunctionType and \
           type(a) is not types.MethodType:
            raise ValueError("Must be a function or method")

        self._cont = a

    @staticmethod
    def return_(a):
        return Cont(a)

    # Bind operator
    # (>>=) :: m a -> (a -> m b) -> m b
    def __ge__(self, f):
        if type(f) is not types.FunctionType and \
           type(f) is not types.MethodType:
            raise ValueError("Must be a function or method")

        return Cont(lambda k: Cont.runCont(self, lambda a: Cont.runCont(f(a), k)))

    # Run a continuation
    # runCont :: Cont r a -> (a -> r) -> r
    @staticmethod
    def runCont(c, f):
        return c._cont(f)


# return_ :: a -> Cont r a
def return_(a):
    return Cont.return_(lambda k: k(a))


# Call current continuation
# callCC :: ((a -> Cont r b) -> Cont r a) -> Cont r a
def callCC(f):
    if type(f) is not types.FunctionType and \
       type(f) is not types.MethodType:
        raise ValueError("Must be a function or method")

    def function(k):
        def function_arg(a):
            return Cont(lambda x: k(a))
        return Cont.runCont(f(function_arg), k)

    return Cont(function)
