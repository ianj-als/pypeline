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
from pypeline.core.types.monad import Maybe


#
# Nothing. This is a singleton.
#
class Nothing(Maybe):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Nothing, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def return_(self, a):
        return return_(a)

    def __ge__(self, function):
        return Nothing()

    def __repr__(self):
        return "<Nothing>"

    def __nonzero__(self):
        return False


def return_(a):
    return Nothing()
