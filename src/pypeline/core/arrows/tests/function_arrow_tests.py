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
import unittest

from pypeline.core.arrows.function_arrow import FunctionArrow, split, unsplit


class ArrowUnitTests(unittest.TestCase):
    #
    # Arrow law tests
    #

    # arr id = id
    def test_identity(self):
        iden = lambda x: x
        arrow = FunctionArrow(iden)
        value = "My old man's a dustman"
        self.assertEquals(iden(value), arrow(value))


    # arr (f . g) = arr f >>> arr g
    def test_arrow_func_comp_is_comp_arrow(self):
        f = lambda x: x * 3;
        g = lambda x: x + 9;
        c = lambda x: g(f(x))

        arrow_func_comp = FunctionArrow(c)
        arrow_comp = FunctionArrow(f) >> FunctionArrow(g)

        value = 7

        self.assertEquals(arrow_func_comp(value), arrow_comp(value))


    # first (arr f) = arr (first f)
    def first_arr_f_is_arr_first_f(self):
        f = lambda x: x + 1
        fst = lambda x: x[0] + 1

        arrow_one = FunctionArrow(f).first()
        arrow_two = FunctionArrow(fst)

        value = (8, -10)
        self.assertEquals(arrow_one(value), arrow_two(value))


    # first (a >>> b) = first a >>> first b
    def test_first_a_b_is_first_a_first_b(self):
        a = lambda x: x * 9
        b = lambda x: x - 7
        c = lambda x: b(a(x))

        arrow_one = FunctionArrow(c).first()
        arrow_two = FunctionArrow(a).first() >> FunctionArrow(b).first()

        value = (7, 21)
        self.assertEquals(arrow_one(value), arrow_two(value))


    # first f >>> arr fst = arr fst >>> f
    def test_first_arrow_fst_is_arrow_fst_func(self):
        fst = lambda x: x[0]
        f = lambda x: x * -9

        arrow_one = FunctionArrow(f).first() >> FunctionArrow(fst)
        arrow_two = FunctionArrow(fst) >> FunctionArrow(f)

        value = (-3, 19)
        self.assertEquals(arrow_one(value), arrow_two(value))


    # first f >>> arr (id *** g) = arr (id *** g) >>> first f
    def first_f_arr_id_g_is_arr_id_g_first_f(self):
        id = lambda x: x
        f = lambda x: x * -3
        g = lambda x: x - 9

        arrow_one = FunctionArrow(f).first() >> (FunctionArrow(id) * FunctionArrow(g))
        arrow_two = (FunctionArrow(id) * FunctionArrow(g)) >> FunctionArrow(f).first()

        value = (-9, 8)
        self.assertEquals(arrow_one(value), arrow_two(value))


    # first (first f) >>> arr assoc = arr assoc >>> first f
    # where assoc((a, b), c) = (a, (b, c))
    def first_first_f_arr_assoc_is_arr_assoc_first_f(self):
        assoc = lambda ab, c: (ab[0], (ab[1], c))
        f = lambda x: x + 3

        arrow_one = FunctionArrow(f).first().first() >> FunctionArrow(assoc)
        arrow_two = FunctionArrow(assoc) >> FunctionArrow(f).first()

        value = ((1, 2), 3)
        self.assertEquals(arrow_one(value), arrow_two(value))


    # arr id >>> a = a = a >>> arr id
    def test_arrow_id_func_is_func_is_func_comp_arrow(self):
        a = lambda x: x + 1
        iden = lambda x: x

        arrow_one = FunctionArrow(iden) >> FunctionArrow(a)
        arrow_two = FunctionArrow(a) >> FunctionArrow(iden)

        value = 9
        self.assertEquals(arrow_one(value), a(value))
        self.assertEquals(arrow_two(value), a(value))


    # first a >>> arr (id x f) = arr (id x f) >>> first a
    # first a >>> second f = second f >>> first a
    def test_first_arr_id_f_is_arr_id_f_first(self):
        a = lambda x: x ** 2
        f = lambda x: x % 3

        arrow_one = FunctionArrow(a).first() >> FunctionArrow(f).second()
        arrow_two = FunctionArrow(f).second() >> FunctionArrow(a).first()

        value = (3, 9)
        self.assertEquals(arrow_one(value), arrow_two(value))


    #
    # Ad hoc tests
    #

    # Basic composition
    def test_composition(self):
        def func_one(b):
            return b * 10
        def func_two(c):
            return c - 9;
        arrow_one = FunctionArrow(func_one)
        arrow_two = FunctionArrow(func_two)
        arrow = arrow_one >> arrow_two
            
        value = 7;
        target = func_two(func_one(7))
        result = arrow(value)

        self.assertEquals(target, result)


    # Basic first
    def test_first(self):
        def func(b):
            return b % 3
        arrow = FunctionArrow(func).first()
        value = 7
        value_tuple = (value, value)
        target = (func(value), value)
        result = arrow(value_tuple)
        self.assertEquals(target, result)


    # Basic second
    def test_second(self):
        def func(b):
            return b % 3
        arrow = FunctionArrow(func).second()
        value = 7
        value_tuple = (value, value)
        target = (value, func(value))
        result = arrow(value_tuple)
        self.assertEquals(target, result)


    # Compose split then first
    def test_split_first(self):
        def func(b):
            return b % 2;
        arrow = split() >> FunctionArrow(func).first()

        value = 7
        target = (func(value), value)
        result = arrow(value)

        self.assertEquals(target, result)


    # (***)
    def test_three_stars(self):
        def f(b):
            return b / 2
        def g(b):
            return (3 * b) + 1

        #        +----------+     +----------+
        #  b --->+---> f ---+---->+----------+---> c
        #        |          |     |          |
        # b' --->+----------+---->+---> g ---+---> c'
        #        +----------+     +----------+
        arrow = FunctionArrow(f) ** FunctionArrow(g)
        value = (5, 7)
        target = (f(value[0]), g(value[1]))
        result = arrow(value)

        self.assertEquals(target, result)


    #
    # (&&&)
    #
    def test_three_ampersands(self):
        def f(b):
            return b / 2
        def g(b):
            return (3 * b) + 1

        #       +-------+     +----------+     +----------+
        #       |   /---+---->+---> f ---+---->+----------+---> c
        # b --->+---    |     |          |     |          |
        #       |   \---+---->+----------+---->+---> g ---+---> d
        #       +-------+     +----------+     +----------+
        arrow = FunctionArrow(f) & FunctionArrow(g)
        value = 5
        target = (f(5), g(5))
        result = arrow(value)
        
        self.assertEquals(target, result)


    # The arrow example from http://www.haskell.org/haskellwiki/Arrow_tutorial
    # A more complex test
    def test_split_unsplit(self):
        #           +------> f ---------+
        #           |                   v
        # 8 ---> (split)          (unsplit (op)) ----> 29
        #           |                   ^
        #           +------> g ---------+
        arrow = split() >> FunctionArrow(lambda b : b / 2).first() >> FunctionArrow(lambda b : (3 * b) + 1).second() >> unsplit(lambda b, c: b + c)
        value = 8
        target = 29
        result = arrow(value)

        self.assertEquals(target, result)


    # Equivalent arrow circuits
    # From http://www.haskell.org/haskellwiki/Arrow_tutorial
    def test_equivalent_arrow(self):
        def f(b):
            return b / 2
        def g(b):
            return (3 * b) + 1
        def split_func(x):
            return (x, x)
        def swap_func(a_tuple):
            return (a_tuple[1], a_tuple[0])
        def add_func(a_tuple):
            return a_tuple[0] + a_tuple[1]

        # Circuit one
        # arr (\x -> (x, x)) >>> first f >>> arr (\(y, x) -> (x, y)) >>> first g >>> arr (\(z, y) -> y + z)
        arrow_one = FunctionArrow(split_func) >> FunctionArrow(f).first() >> FunctionArrow(swap_func) >> FunctionArrow(g).first() >> FunctionArrow(add_func)

        # Circuit two
        # f &&& g >>> arr (\(y, z) -> y + z)
        arrow_two = (FunctionArrow(f) & FunctionArrow(g)) >> FunctionArrow(add_func)

        value = 7
        arg = (f(value), g(value))
        target = add_func(arg)
        result_one = arrow_one(value)
        result_two = arrow_two(value)
        
        self.assertEquals(target, result_one)
        self.assertEquals(target, result_two)
