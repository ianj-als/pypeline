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

from pypeline.core.arrows.function_arrow import FunctionArrow
from pypeline.core.arrows.kleisli_arrow_choice import KleisliArrowChoice
from pypeline.core.arrows.kleisli_arrow import KleisliArrow, split as kleisli_split, unsplit as kleisli_unsplit
from pypeline.core.types.either import Left, Right
from pypeline.core.types.just import Just, return_ as just_return
from pypeline.core.types.state import State, return_ as state_return


class KleisliArrowChoiceUnitTest(unittest.TestCase):
    def test_left_with_maybe_monad(self):
        value = 9
        f = lambda x: x * 9
        k = KleisliArrowChoice(just_return, lambda a: Just(f(a))).left()

        left = KleisliArrow.runKleisli(k, Left(value))
        self.assertEquals(Just(Left(f(value))), left)

        right = KleisliArrow.runKleisli(k, Right(value))
        self.assertEquals(Just(Right(value)), right)


    def test_left_with_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k = KleisliArrowChoice(state_return, f).left()

        value = 3.141
        left_state = KleisliArrow.runKleisli(k, Left(value))
        left = State.runState(left_state, [])
        left_target = (Left(w(value)), [s1])
        self.assertEquals(left_target, left)

        right_state = KleisliArrow.runKleisli(k, Right(value))
        right = State.runState(right_state, [])
        right_target = (Right(value), [])
        self.assertEquals(right_target, right)


    def test_right_with_maybe_monad(self):
        value = 9
        f = lambda x: x * 9
        k = KleisliArrowChoice(just_return, lambda a: Just(f(a))).right()

        left = KleisliArrow.runKleisli(k, Left(value))
        self.assertEquals(Just(Left(value)), left)

        right = KleisliArrow.runKleisli(k, Right(value))
        self.assertEquals(Just(Right(f(value))), right)


    def test_right_with_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k = KleisliArrowChoice(state_return, f).right()

        value = 3.141
        left_state = KleisliArrow.runKleisli(k, Left(value))
        left = State.runState(left_state, [])
        left_target = (Left(value), [])
        self.assertEquals(left_target, left)

        right_state = KleisliArrow.runKleisli(k, Right(value))
        right = State.runState(right_state, [])
        right_target = (Right(w(value)), [s1])
        self.assertEquals(right_target, right)


    def test_triple_add_with_maybe_monad(self):
        value = 11
        f = lambda x: x * 9
        k1 = KleisliArrowChoice(just_return, lambda a: Just(f(a)))

        h = lambda x: x - 9
        k2 = KleisliArrowChoice(just_return, lambda a: Just(h(a)))

        arrow = k1 + k2

        left = KleisliArrow.runKleisli(arrow, Left(value))
        left_target = Just(Left(f(value)))
        self.assertEquals(left_target, left)

        right = KleisliArrow.runKleisli(arrow, Right(value))
        right_target = Just(Right(h(value)))
        self.assertEquals(right_target, right)


    def test_triple_add_with_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k1 = KleisliArrowChoice(state_return, f)

        s2 = "-9"
        y = lambda a: a - 9
        h = lambda a: State(lambda s: (y(a), s.append(s2) or s))
        k2 = KleisliArrowChoice(state_return, h)
        
        arrow = k1 + k2

        value = 19
        left_state = KleisliArrow.runKleisli(arrow, Left(value))
        left = State.runState(left_state, [])
        left_target = (Left(w(value)), [s1])
        self.assertEquals(left_target, left)

        right_state = KleisliArrow.runKleisli(arrow, Right(value))
        right = State.runState(right_state, [])
        right_target = (Right(y(value)), [s2])
        self.assertEquals(right_target, right)


    def test_triple_pipe_with_maybe_monad(self):
        value = 11
        f = lambda x: x * 9
        k1 = KleisliArrowChoice(just_return, lambda a: Just(f(a)))

        h = lambda x: x - 9
        k2 = KleisliArrowChoice(just_return, lambda a: Just(h(a)))

        arrow = k1 | k2

        left = KleisliArrow.runKleisli(arrow, Left(value))
        left_target = Just(f(value))
        self.assertEquals(left_target, left)

        right = KleisliArrow.runKleisli(arrow, Right(value))
        right_target = Just(h(value))
        self.assertEquals(right_target, right)


    def test_triple_pipe_with_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k1 = KleisliArrowChoice(state_return, f)

        s2 = "-9"
        y = lambda a: a - 9
        h = lambda a: State(lambda s: (y(a), s.append(s2) or s))
        k2 = KleisliArrowChoice(state_return, h)
        
        arrow = k1 | k2

        value = 19
        left_state = KleisliArrow.runKleisli(arrow, Left(value))
        left = State.runState(left_state, [])
        left_target = (w(value), [s1])
        self.assertEquals(left_target, left)

        right_state = KleisliArrow.runKleisli(arrow, Right(value))
        right = State.runState(right_state, [])
        right_target = (y(value), [s2])
        self.assertEquals(right_target, right)
