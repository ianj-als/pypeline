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
import subprocess
import types

from pypeline.core.arrows.kleisli_arrow import KleisliArrow, split, unsplit
from pypeline.core.types.state import State, return_


def cons_subprocess_component(process_pipe,
                              input_forming_function,
                              output_forming_function,
                              state_mutator = None):
    """Construct a pipeline component using a Popen object. Subprocesses shall accept a single line on stdin and generate a single line on stdout. Input and output forming functions shall be provided to generate and parse single lines of text that will be used to communicate with the subprocess. The returned object shall be a Kleisli arrow representing this pipeline component."""
    if not isinstance(process_pipe, subprocess.Popen):
        raise ValueError("Must be a Popen process")

    if input_forming_function is None or \
       output_forming_function is None:
        raise ValueError("Subprocess components must specify both " +
                         "input and output forming functions")

    #
    # This bind function handles the 'process'
    # being a subprocess.
    #
    def bind_function(a):
        def state_function(s):
            # Transform the value into a line, that when
            # injected into stdin, the subprocess will understand
            transformed_a = input_forming_function(a, s)

            # Communicate with the subprocess
            if transformed_a is not None:
                print >> process_pipe.stdin, str(transformed_a).strip()
                process_pipe.stdin.flush()
                new_a = process_pipe.stdout.readline().strip()

            # Parse the output from the subprocess
            transformed_new_a = output_forming_function(new_a, s)

            # Mutate the state
            next_s = state_mutator(s) if state_mutator else s

            # New value/state pair
            return (transformed_new_a, next_s)
        return State(state_function)

    return KleisliArrow(return_, bind_function)


def cons_batch_subprocess_component(process_pipe,
                                    input_generator_function,
                                    output_function,
                                    state_mutator = None):
    """Construct a pipeline component using a Popen object. Batch subprocesses shall accept a single line on stdin. An input generator function shall be provided that yields objects, that once "stringyfied", are presented to the subprocess' stdin. This function takes tow arguments: the value and the state objects. It is the responsibility of the feed function implementer to yield an EOF if necessary. The returned object shall be a Kleisli arrow representing this pipeline component."""
    if not isinstance(process_pipe, subprocess.Popen):
        raise ValueError("Must be a Popen process")

    if input_generator_function is None or output_function is None:
        raise ValueError("Subprocess components must specify both " +
                         "input generator and output functions")

    #
    # This bind function handles the 'process'
    # being a subprocess.
    #
    def bind_function(a):
        def state_function(s):
            # The input forming function is an iterable, so
            # request every value this function will return
            # and feed it to the underlying subprocess.
            # This function shall return a value, that when stringyfied and
            # injected into stdin, the subprocess will understand
            for transformed_a in input_generator_function(a, s):
                # Communicate with the subprocess
                if transformed_a is not None:
                    print >> process_pipe.stdin, str(transformed_a).strip()
                    process_pipe.stdin.flush()

            # Get the new a
            new_a = output_function(a, s)

            # Mutate the state
            next_s = state_mutator(s) if state_mutator else s

            # New value/state pair
            return (new_a, next_s)
        return State(state_function)

    return KleisliArrow(return_, bind_function)


def cons_function_component(function,
                            input_forming_function = None,
                            output_forming_function = None,
                            state_mutator = None):
    """Construct a component based on a function. Any input or output forming functions shall be called if provided. In this mode only the Kleisli arrow is returned."""
    if type(function) is not types.FunctionType and \
       type(function) is not types.MethodType:
        raise ValueError("Must be a function or method")

    def bind_function(a):
        def state_function(s):
            # Transform the input
            transformed_a = input_forming_function(a, s) if input_forming_function else a

            # Apply
            new_a = function(transformed_a, s)

            # Transform the output of the function
            transformed_new_a = output_forming_function(new_a, s) if output_forming_function else new_a

            # Mutate the state
            next_s = state_mutator(s) if state_mutator else s

            # New value/state pair
            return (transformed_new_a, next_s)
        return State(state_function)

    return KleisliArrow(return_, bind_function)


def cons_wire(schema_conv_function):
    """Construct a wire. A wire is a Kleisli arrow that converts data from from one pipeline component's output schema to another pipeline component's input schema."""
    def bind_function(a):
        def state_function(s):
            return (schema_conv_function(a, s), s)
        return State(state_function)
    return KleisliArrow(return_, bind_function)


def cons_dictionary_wire(conversions):
    """Construct a wire that converts between two dictionaries. The keys of the conversions dictionary are keys in the output dictionary, of the preceeding component, whose values will be used to populate a dictionary whose keys are the value of the conversions dictionary.\n\nE.g., output = {'int': 9, 'string': 'hello'}, and conversions = {'int': 'int_two', 'string': 'string_two'}, yields an input dictionary, to the next component, input = {'int_two': 9, 'string_two': 'hello'}."""
    return cons_wire(lambda a, _: {conversions[key]: a[key] for key in conversions})


def cons_split_wire():
    """Construct a wire that duplicates its input and produces a pair from this value. See: ***, first, second, and unsplit arrow operators."""
    return split(return_)


def cons_unsplit_wire(unsplit_func):
    """Construct a wire that takes a pair and applies a function to this pair to combine them into one value."""
    return unsplit(return_, unsplit_func)


def cons_wired_components(component_one, component_two, wire):
    """Wire two components together and return a component that is the composition of these components."""
    return component_one >> wire >> component_two


def cons_pipeline(input_wire, component, output_wire):
    """Prepend an input wire and append an output wire to a component to build a pipeline."""
    return input_wire >> component >> output_wire


def cons_composed_component(first_component, second_component):
    """Compose two components and return a component that represents the composed computation."""
    return first_component >> second_component


def cons_parallel_component(top_component, bottom_component):
    """Construct a component that will compute the provided components in parallel. The returned component takes a pair as input, see cons_split_wire(), and the component shall return a pair."""
    return top_component ** bottom_component


def __kleisli_wrapper(f):
    def wrapper(pipeline, input, state):
        """Run, evaluate, or execute a pipeline."""
        state_monad = KleisliArrow.runKleisli(pipeline, input)
        return f(state_monad, state)
    return wrapper


@__kleisli_wrapper
def run_pipeline(state_monad, state):
     return State.runState(state_monad, state)


@__kleisli_wrapper
def eval_pipeline(state_monad, state):
    return State.evalState(state_monad, state)


@__kleisli_wrapper
def exec_pipeline(state_monad, state):
    return State.execState(state_monad, state)
