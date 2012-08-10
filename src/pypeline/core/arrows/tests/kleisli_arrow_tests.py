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
from pypeline.core.arrows.kleisli_arrow import KleisliArrow
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
