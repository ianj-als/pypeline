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


#
# Base monad class
#
class Monad(object):
    # return
    # return :: a -> m a
    def return_(self, a):
        raise NotImplementedError

    # Bind operator
    # (>>=) :: m a -> (a -> m b) -> m b
    def __ge__(self, other):
        raise NotImplementedError

    # Bind "Shove" operator
    # (>>) :: m a -> m b -> m b
    def __rshift__(self, other):
        if not isinstance(other, Monad):
            raise ValueError("Must be a monadic type")
        return self >= (lambda _: other)


#
# Erm, maybe...
#
class Maybe(Monad):
    def __init__(self):
        super(Monad, self).__init__()

