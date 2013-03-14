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
     run_pipeline, \
     eval_pipeline, \
     exec_pipeline


class ParallelPypelineHelperUnitTest(unittest.TestCase):
     @staticmethod
     def test(no_workers, pipeline, input, state, run_function = run_pipeline):
          executor = ThreadPoolExecutor(max_workers = no_workers)
          result = run_function(executor, pipeline, input, state)
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
          top_msg = "top"
          bottom_msg = "bottom"

          reverse_func = lambda a, s: a[::-1]
          top_func = lambda a, s: " ".join([a, top_msg])
          bottom_func = lambda a, s: " ".join([a, bottom_msg])

          comp_rev_top = cons_function_component(reverse_func,
                                                 state_mutator = lambda s: s.append(rev_msg_one) or s)
          comp_rev_bottom = cons_function_component(reverse_func,
                                                    state_mutator = lambda s: s.append(rev_msg_two) or s)
          comp_para_top = cons_function_component(top_func,
                                                  state_mutator = lambda s: s.append(top_msg) or s)
          comp_para_bottom = cons_function_component(bottom_func,
                                                     state_mutator = lambda s: s.append(bottom_msg) or s)

          unsplit_func = lambda t, b: {'top': t, 'bottom': b}

          pipeline = (comp_rev_top & comp_rev_bottom) >> \
                     (comp_para_top ** comp_para_bottom) >> \
                     cons_unsplit_wire(unsplit_func)

          value = "hello world"
          target = (unsplit_func(top_func(reverse_func(value, None), None),
                                 bottom_func(reverse_func(value, None), None)),
                    [rev_msg_one, rev_msg_two, top_msg, bottom_msg])

          result = ParallelPypelineHelperUnitTest.test(2, pipeline, "hello world", list())
          
          self.assertEquals(target, result)


     def test_parallel_run_eval_and_exec(self):
          value = "hello world"
          state = 0

          input_msg = "input"
          output_msg = "output"

          input_func = lambda a, s: " ".join([input_msg, a])
          output_func = lambda a, s: " ".join([a, output_msg])
          function = lambda a, s: a.upper()
          composition = lambda a, s: output_func(function(input_func(a, s), s), s)
          state_func = lambda s: s + 1

          pipeline = cons_function_component(function,
                                             input_func,
                                             output_func,
                                             state_mutator = state_func)

          result = ParallelPypelineHelperUnitTest.test(1, pipeline, value, state, run_pipeline)
          target = (composition(value, state), state_func(state))
          self.assertEquals(target, result)

          result = ParallelPypelineHelperUnitTest.test(1, pipeline, value, state, eval_pipeline)
          target = composition(value, state)
          self.assertEquals(target, result)

          result = ParallelPypelineHelperUnitTest.test(1, pipeline, value, state, exec_pipeline)
          target = state_func(state)
          self.assertEquals(target, result)


     def test_parallel_wire(self):
          value = {'PI' : 3.141, 'E' : 2.718}
          pipeline = cons_wire(lambda a, s: {'pi' : a['PI'], 'e' : a['E']})
          result = ParallelPypelineHelperUnitTest.test(1, pipeline, value, None, eval_pipeline)
          self.assertEquals({'pi' : 3.141, 'e' : 2.718}, result)


     def test_parallel_dictionary_wire(self):
          value = {'pi' : 3.141, 'e' : 2.718}
          pipeline = cons_dictionary_wire({'pi' : 'PI', 'e' : 'E'})
          result = ParallelPypelineHelperUnitTest.test(1, pipeline, value, None, eval_pipeline)
          self.assertEquals({'PI' : 3.141, 'E' : 2.718}, result)
