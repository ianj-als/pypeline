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
from pypeline.core.arrows.kleisli_arrow import KleisliArrow, split as kleisli_split, unsplit as kleisli_unsplit
from pypeline.core.types.just import Just, return_ as just_return
from pypeline.core.types.state import State, return_ as state_return


class KleisliArrowUnitTest(unittest.TestCase):
    def test_run(self):
        value = 7
        f = lambda x: x * 2
        k = KleisliArrow(just_return, lambda a: Just(f(a)))
        self.assertEquals(Just(f(value)), KleisliArrow.runKleisli(k, value))


    def test_kleisli_compose_with_function_arrow(self):
        value = 7
        f = lambda x: x * 2
        head = KleisliArrow(just_return, lambda a: Just(f(a)))
        arrow = head >> head.arr(f) >> head.arr(lambda x: x)
        self.assertEquals(Just(f(f(value))), KleisliArrow.runKleisli(arrow, value))


    # This is mostly lifted from:
    # Programming with arrows - John Hughes
    #   http://www.cse.chalmers.se/~rjmh/afp-arrows.pdf
    def test_word_counter_pipeline(self):
        sentence = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam lectus ligula, ultricies eget placerat vitae, condimentum ut lacus. Donec congue ipsum in lorem posuere porttitor. Nam nibh neque, volutpat ac ultrices nec, mollis a orci. Etiam ac ultrices turpis. Maecenas nec adipiscing nunc. Aenean laoreet vestibulum molestie. Ut bibendum tellus et lorem viverra eu fermentum nibh dictum. Nunc in eleifend erat. Mauris sit amet neque enim, ac bibendum quam. Pellentesque purus est, lacinia quis rhoncus vitae, pulvinar non tellus. Sed id mi et eros eleifend scelerisque. Quisque orci odio, porttitor ut viverra ac, consequat a ante. Nunc eget augue quis."""
        word = "ipsum"
        iden = lambda x: Just(x)
        words = lambda x: x.split()
        filter_ = lambda x: filter(lambda w: w == word, x)
        length = lambda x: len(x)

        head = KleisliArrow(just_return, iden)
        arrow = head >> head.arr(words) >> head.arr(filter_) >> head.arr(length) >> KleisliArrow(just_return, iden)
        self.assertEquals(Just(length(filter_((words(sentence))))), KleisliArrow.runKleisli(arrow, sentence))


    def test_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k1 = KleisliArrow(state_return, f)

        s2 = "-9"
        x = lambda a: a - 9
        h = lambda a: State(lambda s: (x(a), s.append(s2) or s))
        k2 = KleisliArrow(state_return, h)

        arrow = k1 >> k2

        value = 5
        state = list()
        state_monad = KleisliArrow.runKleisli(arrow, value) # This is the value
        self.assertEquals((x(w(value)), [s1, s2]), State.runState(state_monad, state)) # This is the state


    def test_first_with_maybe_monad(self):
        w = lambda a: a * 2
        wk = lambda a: Just(w(a))
        arrow = KleisliArrow(just_return, wk).first()

        value = 9
        result = KleisliArrow.runKleisli(arrow, (value, value))
        target = Just((w(value), value))
        self.assertEquals(target, result)


    def test_second_with_maybe_monad(self):
        w = lambda a: a * 2
        wk = lambda a: Just(w(a))
        arrow = KleisliArrow(just_return, wk).second()

        value = 9
        result = KleisliArrow.runKleisli(arrow, (value, value))
        target = Just((value, w(value)))
        self.assertEquals(target, result)


    def test_first_with_state_monad(self):
        w = lambda a: a * 2
        s1 = "*2"
        wk = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        arrow = KleisliArrow(state_return, wk).first()

        value = 9
        state = KleisliArrow.runKleisli(arrow, (value, value))
        result = State.runState(state, list())
        target = ((w(value), value), [s1])
        self.assertEquals(target, result)


    def test_second_with_state_monad(self):
        w = lambda a: a * 2
        s1 = "*2"
        wk = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        arrow = KleisliArrow(state_return, wk).second()

        value = 9
        state = KleisliArrow.runKleisli(arrow, (value, value))
        result = State.runState(state, list())
        target = ((value, w(value)), [s1])
        self.assertEquals(target, result)


    def test_triple_asterisk_with_maybe_monad(self):
        w = lambda a: a * 2
        wk = lambda a: Just(w(a))
        k1 = KleisliArrow(just_return, wk)

        x = lambda a: a - 9
        xk = lambda a: Just(x(a))
        k2 = KleisliArrow(just_return, xk)

        arrow = k1 ** k2

        value = 7
        target = Just((w(value), x(value)))
        result = KleisliArrow.runKleisli(arrow, (value, value))
        self.assertEquals(target, result)


    def test_triple_ampersand_with_maybe_monad(self):
        w = lambda a: a * 2
        wk = lambda a: Just(w(a))
        k1 = KleisliArrow(just_return, wk)

        x = lambda a: a - 9
        xk = lambda a: Just(x(a))
        k2 = KleisliArrow(just_return, xk)

        arrow = k1 & k2

        value = 7
        target = Just((w(value), x(value)))
        result = KleisliArrow.runKleisli(arrow, value)
        self.assertEquals(target, result)


    def test_triple_ampersand_with_state_monad(self):
        s1 = "*2"
        w = lambda a: a * 2
        f = lambda a: State(lambda s: (w(a), s.append(s1) or s))
        k1 = KleisliArrow(state_return, f)

        s2 = "-9"
        x = lambda a: a - 9
        h = lambda a: State(lambda s: (x(a), s.append(s2) or s))
        k2 = KleisliArrow(state_return, h)

        arrow = k1 & k2

        value = 5
        state = list()
        state_monad = KleisliArrow.runKleisli(arrow, value)

        target = ((w(value), x(value)), [s1, s2])
        result = State.runState(state_monad, state)
        self.assertEquals(target, result)


    def test_split_with_maybe_monad(self):
        value = 7
        arrow = kleisli_split(just_return)
        result = KleisliArrow.runKleisli(arrow, value)
        target = Just((value, value))
        self.assertEquals(target, result)


    def test_split_with_state_monad(self):
        value = 7
        arrow = kleisli_split(state_return)
        state = KleisliArrow.runKleisli(arrow, value)
        result = State.runState(state, list())
        target = ((value, value), list())
        self.assertEquals(target, result)


    def test_unsplit_with_maybe_monad(self):
        value = 8

        k1 = kleisli_split(just_return)

        f = lambda x, y: x * y
        k2 = kleisli_unsplit(just_return, f)

        arrow = k1 >> k2
        
        result = KleisliArrow.runKleisli(arrow, value)
        target = Just(f(value, value))
        self.assertEquals(target, result)


    def test_unsplit_with_state_monad(self):
        value = 7

        k1 = kleisli_split(state_return)

        f = lambda x, y: x * y
        k2 = kleisli_unsplit(state_return, f)

        arrow = k1 >> k2

        state = KleisliArrow.runKleisli(arrow, value)
        result = State.runState(state, list())
        target = (f(value, value), list())
        self.assertEquals(target, result)
