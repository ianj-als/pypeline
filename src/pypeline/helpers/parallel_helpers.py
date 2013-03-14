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
from concurrent.futures import Future
from pypeline.core.arrows.kleisli_arrow import KleisliArrow, split, unsplit
from pypeline.core.types.state import State, return_
from pypeline.helpers import helpers


class WrappedState(object):
    def __init__(self, executor, state):
        self.executor = executor
        self.state = state


def cons_function_component(function,
                            input_forming_function = None,
                            output_forming_function = None,
                            state_mutator = None):
    """Construct a component based on a function. Any input or output forming functions shall be called if provided. A Kleisli arrow is returned."""
    def bind_function(future):
        def state_function(wrapped_state):
            # Unpack state
            state = wrapped_state.state

            def do_transformation(a, s):
                # Transform the input
                transformed_a = input_forming_function(a, state) if input_forming_function else a

                # Apply
                new_a = function(transformed_a, state)

                # Transform the output of the function
                transformed_new_a = output_forming_function(new_a, state) if output_forming_function else new_a

                return transformed_new_a

            # Execute
            new_future = wrapped_state.executor.submit(do_transformation, future.result(), state)

            # Mutate the state
            next_state = state_mutator(state) if state_mutator else state

            # New value/state pair
            return (new_future, WrappedState(wrapped_state.executor, next_state))
        return State(state_function)

    return KleisliArrow(return_, bind_function)


def cons_wire(schema_conv_function):
    """Construct a wire. A wire is a Kleisli arrow that converts data from from one pipeline component's output schema to another pipeline component's input schema."""
    def get_wire_wrapper(inner_function):
        def wire_wrapper(future, wrapper_state):
            new_value = inner_function(future.result(), wrapper_state.state)
            nf = Future()
            nf.set_result(new_value)
            return nf
        return wire_wrapper

    return helpers.cons_wire(get_wire_wrapper(schema_conv_function))


def cons_dictionary_wire(conversions):
    """Construct a wire that converts between two dictionaries. The keys of the conversions dictionary are keys in the output dictionary, of the preceeding component, whose values will be used to populate a dictionary whose keys are the value of the conversions dictionary.\n\nE.g., output = {'int': 9, 'string': 'hello'}, and conversions = {'int': 'int_two', 'string': 'string_two'}, yields an input dictionary, to the next component, input = {'int_two': 9, 'string_two': 'hello'}."""
    return cons_wire(helpers.get_dictionary_conversion_function(conversions))


def cons_split_wire():
    """Construct a wire that duplicates its input and produces a pair from this value. See: ***, first, second, and unsplit arrow operators."""
    return split(return_)


def cons_unsplit_wire(unsplit_function):
    """Construct a wire that takes a pair and applies a function to this pair to combine them into one value."""
    def get_unsplit_wrapper(inner_function):
        def unsplit_wrapper(top_future, bottom_future):
            t_val = top_future.result()
            b_val = bottom_future.result()
            nf = Future()
            nf.set_result(inner_function(t_val, b_val))
            return nf
        return unsplit_wrapper
    
    return unsplit(return_, get_unsplit_wrapper(unsplit_function))


def __kleisli_wrapper(f):
    def wrapper(executor, pipeline, input, state):
        """Run, evaluate, or execute a pipeline."""
        future = Future()
        future.set_result(input)
        state_monad = KleisliArrow.runKleisli(pipeline, future)
        return f(state_monad, WrappedState(executor, state))
    return wrapper


@__kleisli_wrapper
def run_pipeline(state_monad, state):
     output = State.runState(state_monad, state)
     return (output[0].result(), output[1].state)


@__kleisli_wrapper
def eval_pipeline(state_monad, state):
    future = State.evalState(state_monad, state)
    return future.result() 


@__kleisli_wrapper
def exec_pipeline(state_monad, state):
    wrapped_state = State.execState(state_monad, state)
    return wrapped_state.state
