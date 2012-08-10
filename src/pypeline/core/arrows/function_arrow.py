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
# ** is higher than >> is higher than than &
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
