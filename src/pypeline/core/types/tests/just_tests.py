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

from pypeline.core.types.just import Just, return_


class JustMonadUnitTest(unittest.TestCase):
    def test_bind(self):
        value = 9
        f = lambda a: a * 10
        j = return_(value)
        monad = j >= (lambda a: Just(f(a)))

        self.assertEquals(Just(f(value)), monad)


    def test_zero(self):
        self.assertTrue(return_(False))
        self.assertTrue(return_(0))
        self.assertTrue(return_(""))
        self.assertTrue(return_(list()))
        self.assertTrue(return_(dict()))


    def test_eq(self):
        self.assertEquals(Just(10), return_(10))


    def test_ne(self):
        self.assertNotEquals(Just(11), return_(10))
        self.assertNotEquals(Just(11), None)
        self.assertNotEquals(Just(11), object())
