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

from pypeline.core.types.nothing import Nothing, return_


class NothingMonadUnitTest(unittest.TestCase):
    def test_bind(self):
        value = 9
        f = lambda a: a * 10
        j = return_(value)
        monad = j >= (lambda a: Just(f(a)))

        self.assertEquals(Nothing(), monad)


    def test_zero(self):
        self.assertFalse(Nothing("nowt"))


    def test_eq(self):
        self.assertTrue(Nothing() == return_("blah"))
        self.assertFalse(Nothing() == None)
        self.assertFalse(Nothing() == object())
