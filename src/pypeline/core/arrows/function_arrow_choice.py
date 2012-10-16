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
from pypeline.core.arrows.arrow import Arrow, ArrowChoice
from pypeline.core.arrows.function_arrow import FunctionArrow
from pypeline.core.types.either import *


class FunctionArrowChoice(ArrowChoice, FunctionArrow):
    def __init__(self, f):
        ArrowChoice.__init__(self)
        FunctionArrow.__init__(self, f)

    #
    # left :: a b c -> a (Either b d) (Either c d)
    #
    #                +-------------------+
    #                |    /--- f ---\    |
    # Either b d --->+---(           )---+---> Either c d
    #                |    \---------/    |
    #                +-------------------+
    def left(self):
        def left_func(either):
            if isinstance(either, Left):
                return Left(self._func(either.val))
            elif isinstance(either, Right):
                return either
            else:
                raise ValueError("Must be of type Either")

        return FunctionArrowChoice(left_func)

    #
    # right :: a b c -> a (Either d b) (Either d c)
    #
    #                +-------------------+
    #                |    /---------\    |
    # Either d b --->+---(           )---+---> Either d c
    #                |    \--- f ---/    |
    #                +-------------------+
    def right(self):
        def right_func(either):
            if isinstance(either, Left):
                return either
            elif isinstance(either, Right):
                return Right(self._func(either.val))
            else:
                raise ValueError("Must be of type Either")

        return FunctionArrowChoice(right_func)

    #
    # (+++) :: a b c -> a b' c' -> a (Either b b') (Either c c')
    #
    #                 +---------------+                   +---------------+
    #                 |   /-- f --\   |                   |   /-------\   |
    # Either b b' --->+--(         )--+--> Either c b' -->+--(         )--+---> Either c c'
    #                 |   \-------/   |                   |   \-- g --/   |
    #                 +---------------+                   +---------------+
    def __add__(self, other):
        if not isinstance(other, FunctionArrowChoice):
            raise ValueError("Must be a FunctionArrow")

        return self.left() >> other.right()

    #
    # (|||) :: a b d -> a c d -> a (Either b c) d
    #
    #                 +---------------+                   +---------------+                   +-------------------+
    #                 |   /-- f --\   |                   |   /-------\   |                   |   /-- Left? --\   |
    # Either b b' --->+--(         )--+--> Either c b' -->+--(         )--+--> Either c c' -->+--(             )--+---> d
    #                 |   \-------/   |                   |   \-- g --/   |                   |   \-- Right? -/   |
    #                 +---------------+                   +---------------+                   +-------------------+
    def __or__(self, other):
        if not isinstance(other, FunctionArrowChoice):
            raise ValueError("Must be a FunctionArrow")

        def merge(either):
            if not isinstance(either, Either):
                raise ValueError("Must be an Either")
            return either.val

        return (self + other) >> FunctionArrow(merge)


#
# Tests a value
#
# test :: a b c -> a b (Either b b)
#
def test(arrow):
    if not isinstance(arrow, FunctionArrow):
        raise ValueError("Must be a FunctionArrow")

    # (a &&& arr id) >>> arr (\(b, x) = if b then Left x else Right x)
    return (arrow & FunctionArrow(lambda x: x)) >> FunctionArrow(lambda t: Left(t[1]) if t[0] else Right(t[1])) 


#
# This maker returns an arrow that implements if
#
# if_maker :: (b -> c) -> (b -> d) -> (b -> d) -> a b (Either d d)
#
def if_maker(predicate_func, then_func, else_func):
    return test(FunctionArrow(predicate_func)) >> (FunctionArrowChoice(then_func) | FunctionArrowChoice(else_func))

   
