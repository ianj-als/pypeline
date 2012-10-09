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
from pypeline.core.arrows.kleisli_arrow import KleisliArrow
from pypeline.core.types.either import *


class KleisliArrowChoice(ArrowChoice, KleisliArrow):
    def __init__(self, patcher, f):
        ArrowChoice.__init__(self)
        KleisliArrow.__init__(self, patcher, f)

    # left :: a b c -> a (Either b d) (Either c d)
    def left(self):
        def left_func(either):
            if isinstance(either, Left):
                return self._func(either.val) >= (lambda a: self._patcher(Left(a)))
            elif isinstance(either, Right):
                return self._patcher(either)
            else:
                raise ValueError("Must be of type Either")

        return KleisliArrowChoice(self._patcher, left_func)

    # right :: a b c -> a (Either d b) (Either d c)
    def right(self):
        def right_func(either):
            if isinstance(either, Right):
                return self._func(either.val) >= (lambda a: self._patcher(Right(a)))
            elif isinstance(either, Left):
                return self._patcher(either)
            else:
                raise ValueError("Must be of type Either")

        return KleisliArrowChoice(self._patcher, right_func)

    # (+++) :: a b c -> a b' c' -> a (Either b b') (Either c c')
    def __add__(self, other):
        if not isinstance(other, KleisliArrowChoice):
            raise ValueError("Must be a KleisliArrowChoice")

        return self.left() >> other.right()

    # (|||) :: a b d -> a c d -> a (Either b c) d
    def __or__(self, other):
        if not isinstance(other, KleisliArrowChoice):
            raise ValueError("Must be a KleisliArrowChoice")

        return (self + other) >> KleisliArrow(other._patcher, lambda either: self._patcher(either.val))
