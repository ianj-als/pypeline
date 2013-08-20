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

from pypeline.core.types.monad import Monad


#
# State monad
#
# See:
#  Publications:
#    http://learnyouahaskell.com/for-a-few-monads-more#state
#    http://book.realworldhaskell.org/read/monads.html
#
#  Tutorial:
#    http://brandon.si/code/the-state-monad-a-tutorial-for-the-confused/
#    http://channel9.msdn.com/Shows/Going+Deep/Brian-Beckman-The-Zen-of-Expressing-State-The-State-Monad
#
class State(Monad):
    def __init__(self, a):
        super(Monad, self).__init__()
        if type(a) is not types.FunctionType and \
           type(a) is not types.MethodType:
            raise ValueError("Must be a function or method")

        self._func = a

    # return
    # return :: a -> m a
    @staticmethod
    def return_(a):
        return State(lambda s: (a, s))

    # (>>=) :: State s a -> (a -> State s b) -> State s b
    # (State h) >>= f = State $ \s -> let (a, newState) = h s
    #                                     (State g) = f a
    #                                 in  g newState
    def __ge__(self, function):
        if type(function) is not types.FunctionType and \
           type(function) is not types.MethodType:
            raise ValueError("Must be a function or method")

        def composition(s):
            a, state = State.runState(self, s)
            new_state_monad = function(a)
            if not isinstance(new_state_monad, State):
                raise ValueError("Bind function [%s] shall return a State monad object" % function)
            return State.runState(new_state_monad, state)

        return State(composition)

    def __repr__(self):
        return "<State: %s>" % self._func

    @staticmethod
    def runState(state, s):
        return state._func(s)

    @staticmethod
    def evalState(state, s):
        result = State.runState(state, s)
        return result[0]

    @staticmethod
    def execState(state, s):
        result = State.runState(state, s)
        return result[1]


def return_(a):
    return State.return_(a)
