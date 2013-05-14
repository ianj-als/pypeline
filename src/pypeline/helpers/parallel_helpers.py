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
from pypeline.helpers.helpers import get_dictionary_conversion_function


#
# Monkey patch the Future class to support indexing
#
Future.__getitem__ = lambda f, key: (f.result())[key]


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

            assert isinstance(future, Future), "Future is not a future! Strange."

            def do_transformation(a, s):
                # Transform the input
                transformed_a = input_forming_function(a, state) if input_forming_function else a

                # Apply
                new_a = function(transformed_a, state)

                # Transform the output of the function
                transformed_new_a = output_forming_function(new_a, state) if output_forming_function else new_a

                return transformed_new_a

            # Execute
            new_future = wrapped_state.executor.submit(do_transformation,
                                                       future.result(),
                                                       state)

            # Mutate the state
            next_state = state_mutator(state) if state_mutator else state
            # New value/state pair
            return (new_future, WrappedState(wrapped_state.executor, next_state))
        return State(state_function)

    return KleisliArrow(return_, bind_function)


def cons_wire(schema_conv_function):
    """Construct a wire. A wire is a Kleisli arrow that converts data from from one pipeline component's output schema to another pipeline component's input schema."""
    def wire_bind_function(a):
        def wire_state_function(s):
            new_a = schema_conv_function(a, s.state)
            if isinstance(a, tuple):
                futured_new_a = [None, None]
                for a_new_a, futured_new_a_idx in zip(new_a, range(len(futured_new_a))):
                    if isinstance(a_new_a, Future):
                        futured_new_a[futured_new_a_idx] = a_new_a
                    else:
                        futured_new_a[futured_new_a_idx] = Future()
                        futured_new_a[futured_new_a_idx].set_result(a_new_a)
                futured_new_a = tuple(futured_new_a)
            else:
                futured_new_a = Future()
                futured_new_a.set_result(new_a)

            return (futured_new_a, s)
        return State(wire_state_function)

    return KleisliArrow(return_, wire_bind_function)


def cons_dictionary_wire(conversions):
    """Construct a wire that converts between two dictionaries. The keys of the conversions dictionary are keys in the output dictionary, of the preceeding component, whose values will be used to populate a dictionary whose keys are the value of the conversions dictionary.\n\nE.g., output = {'int': 9, 'string': 'hello'}, and conversions = {'int': 'int_two', 'string': 'string_two'}, yields an input dictionary, to the next component, input = {'int_two': 9, 'string_two': 'hello'}."""
    return cons_wire(get_dictionary_conversion_function(conversions))


def cons_split_wire():
    """Construct a wire that duplicates its input and produces a pair from this value. See: ***, first, second, and unsplit arrow operators."""
    def split_func(a, s):
        new_a = [None, None]
        if isinstance(a, tuple):
            for an_a, new_a_idx in zip(a, range(len(new_a))):
                if isinstance(an_a, Future):
                    new_a[new_a_idx] = an_a
                else:
                    assert False, "Tuple does not contain futures: %s" % str(a)
        else:
                new_a[0] = Future()
                new_a[1] = Future()
                new_a[0].set_result(a)
                new_a[1].set_result(a)

        return tuple(new_a)
    return cons_function_component(split_func)


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


def __handle_output(o):
    po = (o[0].result() if isinstance(o[0], Future) else o[0],
          o[1].result() if isinstance(o[1], Future) else o[1]) if isinstance(o, tuple) \
         else o.result()
    return po


def __kleisli_wrapper(f):
    def wrapper(executor, pipeline, input, state):
        """Run, evaluate, or execute a pipeline."""
        if isinstance(input, tuple):
            future = (Future(), Future())
            for fu, v in zip(future, input):
                fu.set_result(v)
        else:
            future = Future()
            future.set_result(input)
        state_monad = KleisliArrow.runKleisli(pipeline, future)
        return f(state_monad, WrappedState(executor, state))
    return wrapper


@__kleisli_wrapper
def run_pipeline(state_monad, state):
     output = State.runState(state_monad, state)
     return (__handle_output(output[0]), output[1].state)


@__kleisli_wrapper
def eval_pipeline(state_monad, state):
    future = State.evalState(state_monad, state)
    return __handle_output(future)


@__kleisli_wrapper
def exec_pipeline(state_monad, state):
    wrapped_state = State.execState(state_monad, state)
    return wrapped_state.state
