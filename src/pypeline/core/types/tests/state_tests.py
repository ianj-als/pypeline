import unittest
import inspect

from pypeline.core.types.state import State, return_


class StateMonadUnitTest(unittest.TestCase):
    def test_single_immutable_state(self):
        # Value/state pair
        value = 7
        state = list()

        # Build stuff
        m = return_(value)
        target = (value, state)

        result = State.runState(m, state)
        self.assertEquals(target, result)


    def test_single_mutable_state(self):
        # Value/state pair
        value = 7
        state = list()

        # Build stuff
        m = State(lambda s: (value, s.append(value)))
        target = (value, state.append(value))

        result = State.runState(m, state)
        self.assertEquals(target, result)


    def test_many_mutable_state(self):
        # Build this:
        # state (\s -> (1, s ++ ["Initial value 1"]))
        #    >>= (\a -> state (\s -> (a * 2, s ++ ["Mult by 2"])))
        #    >>= (\a -> state (\s -> (a - 9, s ++ ["Minus 9"])))
        s_one = "Initial value 1"
        s_two = "Multiply by 2"
        s_three = "Minus 9"

        m_one = State(lambda s: (1, s.append(s_one) or s))
        m_two = m_one >= (lambda a: State(lambda s: (a * 2, s.append(s_two) or s)))
        m_three = m_two >= (lambda a: State(lambda s: (a - 9, s.append(s_three) or s)))

        result = State.runState(m_three, list())
        self.assertEquals((-7, [s_one, s_two, s_three]), result)


    def test_with_return(self):
        value = 7
        state = list()
        m = return_(value)

        result = State.runState(m, state)
        self.assertEquals((value, state), result)


    def test_eval_state(self):
        value = 7
        state = list()
        m = return_(value)

        self.assertEquals(value, State.evalState(m, state))


    def test_exec_state(self):
        value = 7
        state = list()
        msg = "*2"
        m_one = return_(value)
        m_two = m_one >= (lambda a: State(lambda s: (a * 2, s.append(msg) or s)))

        self.assertEquals([msg], State.execState(m_two, state))
