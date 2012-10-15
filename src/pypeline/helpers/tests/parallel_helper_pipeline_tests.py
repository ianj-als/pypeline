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
# Unit tests for building a pipeline using the helper functions.
# The pipeline is a mixture of components that are sub-processes and plain old
# Python functions.
#
import os
import subprocess
import sys
import unittest

from concurrent.futures import ThreadPoolExecutor
from pypeline.helpers.parallel_helpers import cons_function_component, \
     cons_wire, \
     cons_dictionary_wire, \
     cons_split_wire, \
     cons_unsplit_wire, \
     run_pipeline


class ParallelPypelineHelperUnitTest(unittest.TestCase):
     @staticmethod
     def test(no_workers, pipeline, input, state):
          executor = ThreadPoolExecutor(max_workers = no_workers)
          result = run_pipeline(executor, pipeline, input, state)
          executor.shutdown(True)
          return result


     def test_serial_pypeline_with_function_components(self):
          rev_msg_one = "reverse(1)"
          rev_msg_two = "reverse(2)"
          upper_msg = "upper"

          reverse_function = lambda a, s: a[::-1]
          upper_function = lambda a, s: a.upper()

          comp_rev_one = cons_function_component(reverse_function,
                                                 state_mutator = lambda s: s.append(rev_msg_one) or s)
          comp_rev_two = cons_function_component(reverse_function,
                                                 state_mutator = lambda s: s.append(rev_msg_two) or s)
          comp_upper = cons_function_component(upper_function,
                                               state_mutator = lambda s: s.append(upper_msg) or s)

          pipeline = comp_rev_one >> comp_rev_two >> comp_upper

          value = "hello world"
          target = (upper_function(value, None), [rev_msg_one, rev_msg_two, upper_msg])
          result = ParallelPypelineHelperUnitTest.test(2, pipeline, "hello world", list())

          self.assertEquals(target, result)


     def test_parallel_pypeline_with_split_and_unsplit_wires(self):
          rev_msg_one = "reverse(top)"
          rev_msg_two = "reverse(bottom)"

          reverse_func = lambda a, s: a[::-1]

          comp_rev_top = cons_function_component(reverse_func,
                                                 state_mutator = lambda s: s.append(rev_msg_one) or s)
          comp_rev_bottom = cons_function_component(reverse_func,
                                                    state_mutator = lambda s: s.append(rev_msg_two) or s)

          unsplit_func = lambda t, b: {'top': t, 'bottom': b}

          pipeline = (comp_rev_top & comp_rev_bottom) >> cons_unsplit_wire(unsplit_func)

          value = "hello world"
          target = (unsplit_func(reverse_func(value, None), reverse_func(value, None)),
                    [rev_msg_one, rev_msg_two])

          result = ParallelPypelineHelperUnitTest.test(2, pipeline, "hello world", list())
          
          self.assertEquals(target, result)
