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

from pypeline.core.types.either import Either, Left, Right


class EitherUnitTests(unittest.TestCase):
    def test_eq(self):
        self.assertEquals(Left(10), Left(10))
        self.assertEquals(Right("something"), Right("something"))


    def test_ne(self):
        self.assertNotEquals(Left(10), Left(11))
        self.assertNotEquals(Left(10), Right(10))
