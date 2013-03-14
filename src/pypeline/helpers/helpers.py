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


def cons_function_component(function,
                            input_forming_function = None,
                            output_forming_function = None,
                            state_mutator = None):
    """Construct a pipeline component whose computation will be achieved using a function. Optional input and output forming functions pre- and post-process the input and output values to and from the function. An optional state mutator function can be provided to alter the state object passed into one of the pipeline run/evaluating/executing functions. A Kleisli arrow is returned."""
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
    return cons_wire(get_dictionary_conversion_function(conversions))


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


def get_dictionary_conversion_function(conversions):
    """Returns a function that completes the dictionary conversions as part of a wire."""
    return lambda a, _: {conversions[key]: a[key] for key in conversions}
