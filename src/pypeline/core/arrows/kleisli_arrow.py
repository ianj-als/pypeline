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

from pypeline.core.arrows.arrow import Arrow


#
# Kleisli arrows of a monad
#
# See:
#  Publications:
#    http://www.cse.chalmers.se/~rjmh/Papers/arrows.pdf
#
class KleisliArrow(Arrow):
    #
    # patcher :: Monad m => a -> m a
    # function :: Monad m => a -> m b
    #
    def __init__(self, patcher, f):
        if not isinstance(patcher, types.FunctionType) and not isinstance(patcher, types.MethodType):
            raise ValueError("Patcher must be a function")
        if f and (not isinstance(f, types.FunctionType) and
                  not isinstance(f, types.MethodType)):
            raise ValueError("Function must be a function")

        Arrow.__init__(self)
        self._patcher = patcher
        self._func = f

    # arr f = K(\b -> return(f b))
    def arr(self, f):
        return KleisliArrow(self._patcher, lambda b: self._patcher(f(b)))

    # K f >>> K g = K(\b -> f b >>= g)
    def __rshift__(self, other):
        if not isinstance(other, KleisliArrow):
            raise ValueError("Must be an KleisliArrow")

        return KleisliArrow(other._patcher, lambda b: self._func(b) >= other._func)

    # K f (***) K g = first K f >>> second K g
    def __pow__(self, other):
        if not isinstance(other, KleisliArrow):
            raise ValueError("Must be an KleisliArrow")

        return self.first() >> other.second()

    # K f &&& K g = K $ \a -> do
    #                           b <- f a
    #                           c <- g a
    #                           return (b,c)
    def __and__(self, other):
        if not isinstance(other, KleisliArrow):
            raise ValueError("Must be an KleisliArrow")

        func = lambda a: self._func(a) >= (lambda b: other._func(a) >= (lambda c: other._patcher((b, c))))
        return KleisliArrow(other._patcher, func)

    # first (K f) = K(\(b, d) -> f b >>= \c -> return (c, d))
    def first(self):
        func = lambda t: self._func(t[0]) >= (lambda c: self._patcher((c, t[1])))
        return KleisliArrow(self._patcher, func)

    # second (K f) = K(\(d, b) -> f b >>= \c -> return (d, c))
    def second(self):
        func = lambda t: self._func(t[1]) >= (lambda c: self._patcher((t[0], c)))
        return KleisliArrow(self._patcher, func)

    @staticmethod
    def runKleisli(k, a):
        if not isinstance(k, KleisliArrow):
            raise ValueError("Arrow must be a Kleisli arrow")
        return k._func(a)


#
# Split
#
def split(patcher):
    return KleisliArrow(patcher, lambda b: patcher((b, b)))


#
# Unsplit
#
def unsplit(patcher, op_func):
    return KleisliArrow(patcher, lambda t: patcher(op_func(t[0], t[1])))
