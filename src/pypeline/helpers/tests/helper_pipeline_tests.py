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

from pypeline.helpers.helpers import cons_subprocess_component, \
     cons_function_component, \
     cons_wire, \
     cons_dictionary_wire, \
     cons_pipeline, \
     wire_components, \
     run_pipeline


class PypelineHelperFunctionUnitTest(unittest.TestCase):
     @staticmethod
     def __cons_and_start_subprocess_component(command,
                                               arguments,
                                               input_forming_func,
                                               output_forming_func,
                                               state_mutator = None):
          args = [command]
          args.extend(arguments)
          pipe = subprocess.Popen(args,
                                  stdin = subprocess.PIPE,
                                  stdout = subprocess.PIPE)
          try:
               arrow = cons_subprocess_component(pipe,
                                                 input_forming_func,
                                                 output_forming_func,
                                                 state_mutator)
          except Exception, ex:
               pipe.terminate()
               pipe.wait()
               raise ex

          return (arrow, pipe)


     def test_pypeline_wth_subprocess_and_function_components(self):
          if sys.platform.startswith('win'):
               self.fail("Currently only this unit test is only supported on non-Windows platforms")
               
          rev_msg_one = "reverse(1)"
          rev_msg_two = "reverse(2)"
          upper_msg = "upper"

          reverse_command = os.path.join("src", "pypeline", "helpers", "tests", "reverse.sh")

          comp_proc_one = PypelineHelperFunctionUnitTest.__cons_and_start_subprocess_component(
               reverse_command, tuple(),
               lambda a, s: str(a['input']),
               lambda a, s: {'output': str(a)},
               state_mutator = lambda s: s.append(rev_msg_one) or s)
          try:
               comp_proc_two = PypelineHelperFunctionUnitTest.__cons_and_start_subprocess_component(
                    reverse_command, tuple(),
                    lambda a, s: str(a['input']),
                    lambda a, s: {'output': str(a)},
                    state_mutator = lambda s: s.append(rev_msg_two) or s)
               try:
                    comp_one = comp_proc_one[0]
                    comp_two = comp_proc_two[0]

                    upper_func = lambda a_string, s: a_string.upper()
                    comp_three = cons_function_component(upper_func,
                                                         state_mutator = lambda s: s.append(upper_msg) or s)

                    input_wire_func = lambda a, s: {'input': a}
                    input_wire = cons_wire(input_wire_func)
    
                    wire = cons_dictionary_wire({'output': 'input'})

                    output_to_string_func = lambda a, s: str(a['output'])
                    to_upper_wire = cons_wire(output_to_string_func)

                    output_wire_func = lambda a, s: str(a['output'])
                    output_wire = cons_wire(output_wire_func)

                    pipeline = input_wire >> wire_components(comp_one, comp_two, wire) >> to_upper_wire >> comp_three

                    value = "hello world"
                    target = (upper_func(value, None), [rev_msg_one, rev_msg_two, upper_msg])
                    result = run_pipeline(pipeline, "hello world", list())

                    self.assertEquals(target, result)
               finally:
                    comp_proc_two[1].terminate()
                    comp_proc_two[1].wait()
          finally:
               comp_proc_one[1].terminate()
               comp_proc_one[1].wait()
