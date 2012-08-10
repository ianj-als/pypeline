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
        if type(a) is types.FunctionType or \
           type(a) is types.MethodType:
            self._func = a
        else:
            self._func = lambda s: (a, s)

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
    return State(a)
