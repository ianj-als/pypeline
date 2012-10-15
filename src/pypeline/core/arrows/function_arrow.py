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
# An implementation of Arrows with functions. The composition
# operator (>>>) is implemented as the right shift
# operator (>>). Tuple input parallel computation (***) is the
# Python (**) operator. And Parallel computation with a scalar
# input (&&&) is the bitwise and operator (&).
# WATCH OUT FOR OPERATOR PRECEDENCE!!!
#
# ** is higher than >> is higher than &
#
#
# See:
#  Publications:
#    http://www.cse.chalmers.se/~rjmh/Papers/arrows.pdf
#    http://www.soi.city.ac.uk/~ross/papers/notation.pdf
#
#  Tutorials:
#    http://www.haskell.org/arrows/
#    http://www.haskell.org/haskellwiki/Arrow_tutorial
#    http://en.wikibooks.org/wiki/Haskell/Understanding_arrows
#
class FunctionArrow(Arrow):
    def __init__(self, func):
        if type(func) is not types.FunctionType and \
           type(func) is not types.MethodType:
            raise ValueError("Must be a function or method")

        Arrow.__init__(self)
        self._func = func

    #
    # (>>>) composition
    #
    #       +---------+           +---------+
    # b --->+--- f ---+--- c ---->+--- g ---+---> d
    #       +---------+           +---------+
    def __rshift__(self, other):
        if not isinstance(other, Arrow):
            raise ValueError("Must be an arrow")

        return FunctionArrow(lambda b: other._func(self._func(b)))

    #
    # (***) parallel computation with input of type tuple
    #
    #       +---------+           +---------+
    # b --->+--- f ---+---> c --->+---------+---> c
    #       |         |           |         |
    # d --->+---------+---> d --->+--- g ---+---> e
    #       +---------+           +---------+
    def __pow__(self, other):
        if not isinstance(other, Arrow):
            raise ValueError("Must be an arrow")

        return self.first() >> other.second()

    #
    # (&&&) parallel computation with scalar input
    #
    #       +---------+           +---------+           +---------+
    #       |    /----+---> b --->+--- f ---+---> c --->+---------+---> c
    # b --->+----     |           |         |           |         |
    #       |    \----+---> b --->+---------+---> b --->+--- g ---+---> d
    #       +---------+           +---------+           +---------+
    def __and__(self, other):
        if not isinstance(other, Arrow):
            raise ValueError("Must be an arrow")

        return split() >> self.first() >> other.second()

    #
    # First
    #
    #       +---------+
    # b --->+--- f ---+---> c
    #       |         |
    # d --->+---------+---> d
    #       +---------+
    def first(self):
        def composition(a_tuple):
            if type(a_tuple) is not types.TupleType:
                raise ValueError("Must be a tuple type")

            return (self._func(a_tuple[0]), a_tuple[1])

        return FunctionArrow(composition)

    #
    # Second
    #
    #       +---------+
    # d --->+---------+---> d
    #       |         |
    # b --->+--- f ---+---> c
    #       +---------+
    def second(self):
        def composition(a_tuple):
            if type(a_tuple) is not types.TupleType:
                raise ValueError("Must be a tuple type")

            return (a_tuple[0], self._func(a_tuple[1]))

        return FunctionArrow(composition)

    #
    # Apply a value, of appropriate type, to the arrow
    #
    def __call__(self, value):
        return self._func(value)


#
# Split
#
#       +-------+
#       |   /---+---> b
# b --->+---    |
#       |   \---+---> b
#       +-------+
def split():
    return FunctionArrow(lambda b: (b, b))


#
# Unsplit
#
#       +---------+
# b --->+---\     |
#       |  (op)---+---> d
# c --->+---/     |
#       +---------+
def unsplit(op_func):
    return FunctionArrow(lambda t: op_func(t[0], t[1]))
