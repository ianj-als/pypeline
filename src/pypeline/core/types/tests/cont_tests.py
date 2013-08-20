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
import os
import sys

from pypeline.core.types.cont import Cont, return_, callCC


class ContMonadUnitTest(unittest.TestCase):
    def test_single_value(self):
        value = 7
        cont = return_(value)
        result = Cont.runCont(cont, lambda x: x)
        self.assertEquals(value, result)


    def test_bind(self):
        square_cps = lambda x: return_(x ** 2)
        add_three_cps = lambda x: return_(x + 3)
        result = Cont.runCont(square_cps(4) >= add_three_cps, lambda x: x)
        self.assertEquals(19, result)
        

    def test_desugared_do_notation(self):
        # do x_squared <- square_cont x
        #    y_squared <- square_cont y
        #    sum_of_squares <- add_cont x_squared y_squared
        #    return sum_of_squares
        add_cps = lambda x, y: return_(x + y)
        square_cps = lambda x: return_(x ** 2)
        pythagoras_cps = lambda x, y: (square_cps(x) >=
                                       ((lambda x_squared: square_cps(y) >=
                                         ((lambda y_squared: add_cps(x_squared, y_squared) >=
                                           (lambda sum_of_squares: return_(sum_of_squares)))))))
        result = Cont.runCont(pythagoras_cps(3, 4), lambda x: x)
        self.assertEquals(25, result)


    def test_call_current_continuation(self):
        # divide_cps :: Int -> Int -> (String -> Cont r Int) -> Cont r Int
        def divide_cps(x, y, k):
            return callCC(lambda ok: callCC(lambda not_ok: not_ok("Divide by zero error") if y is 0 else ok(x / y)) >=
                          (lambda err: k(err)))

        error = lambda err: sys.stderr.write(err + os.linesep)

        print Cont.runCont(divide_cps(10, 2, error), lambda x: x)
        print Cont.runCont(divide_cps(10, 0, error), lambda x: x)
        self.assertTrue(False)
