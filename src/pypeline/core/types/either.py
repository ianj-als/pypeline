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
class Either(object):
    def __hash__(self):
        return self.val.__hash__()


class Left(Either):
    def __init__(self, a):
        super(Left, self).__init__()
        self.val = a

    def __eq__(self, other):
        if not isinstance(other, Left):
            return False
        if id(self) == id(other):
            return True
        if self.val == other.val:
            return True

        return False

    def __repr__(self):
        return "<Left: %s>" % self.val


class Right(Either):
    def __init__(self, b):
        super(Right, self).__init__()
        self.val = b

    def __eq__(self, other):
        if not isinstance(other, Right):
            return False
        if id(self) == id(other):
            return True
        if self.val == other.val:
            return True

        return False

    def __repr__(self):
        return "<Right: %s>" % self.val
