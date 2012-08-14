# Pypeline - An arrow based pipelining library 

Pypeline is licensed using the [GNU Lesser Public License Version 3](http://www.gnu.org/licenses/lgpl.txt).

A pipeline building library based on *arrows*. Arrows are abstractions of computation, and were proposed by [John Hughes](http://www.cse.chalmers.se/~rjmh/) [Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000]. Like monads, arrows provide a general structure for libraries, but are more general; arrows allow multiple inputs and behaviour that is independed of input.

This implementation is heavily inspired by the Haskell arrow typeclasses: a description of which can be found [here](http://www.haskell.org/arrows/index.html).

Arrow introductory reading:
 * Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000
 * Arrows, By Christoph Galliker, June 2010
 * Kleisli arrows of outrageous fortune, Conor McBride, 2011

## Installation

setuptools is required to build, test and install Pypeline. Eggs can be built and installed also.

To install an Egg:

  `sudo python setup.py install bdist_egg`

To view setup help:

  `python setup.py --help`

## Implementation

This Python implementation provides the following arrows:
 * Function arrow,
 * Function choice arrow, and
 * Kleisli arrow (It is expected that the Kleisli choice arrow will be implemented shortly).

And also provides helper functions that lift the arrow abstraction to a *pipeline component* level, in order that pipelines can be constructed without "seeing" an arrow directly. However, if the programmer wishes, the underlying arrow classes can be used to build pipelines with or without the helper functions.

The library also implements some monad classes, primarily, for use with the Kleisli arrow class. These are:
 * Maybe, and
 * State.

## Pipelines

Pipelines can be constructed using the helpers function in the [pypeline.helpers.helpers](https://github.com/ianj-als/pypeline/blob/master/src/pypeline/helpers/helpers.py) module. There are three primatives that can be constructed:
 1. Pipelines,
 2. Pipeline components, and
 3. Wires.

A pipeline is a series of pipeline components that are, optionally, connected with wires. Pipeline components can be constructed with functions, or with a `subprocess.Popen` object; this enables pipelines to be built that call externally running programs. Currently, the protocol for communicating with subprocesses is via stdin and stdout. A single line is fed into the subprocess on stdin and it shall respond with a single line on it's stdout.

Wires can be used to convert the output of one pipeline component into the input of the succeeding pipeline component. Wires can be constructed using a function or a dictionary. Assuming a pipeline component's output is a dictionary and the next component accepts, as input, a dictionary, a wire, constructed from a dictionary, maps values in the output dictionary into a dictionary which is to be used as an input. However, a wire constructed from a function can create arbitrary output to input mappings.

Wires convert the output schema from one pipeline component to the input schema of another component. Wires can be used to join pipelines or components that have been provided by others; where the input and outputs of these may not be compatible with your own implementations.

There are no rules for creating your pipelines. Pipelines, pipeline components, and wires are instances of a Kleisli arrow, and as such any one of these objects can be used as a 'pipeline'. It's up to you how your pipeline is constructed. The helper functions allow the programmer to compose the three conceptual primatives easily.

### Pipeline Functions

#### Constructing a Pipeline
    helpers.cons_pipeline(input_wire, component, output_wire)

Construct a pipeline from a component and two wires. The input wire shall convert a real world input into the expected input for the component, and the output wire shall convert the output from the component into an expected real world value. The funtion returns a `core.arrows.KleisliArrow` object that represents the pipeline.

#### Running a Pipeline
    helpers.run_pipeline(pipeline, input, state)

#### Evaluating a Pipeline
    helpers.eval_pipeline(pipeline, input, state)

#### Executing a Pipeline
    helpers.exec_pipeline(pipeline, input, state)

### Pipeline Component Functions

#### Constructing a Function Based Pipeline Component

    helpers.cons_function_component(function,
                                    input_forming_function = None,
                                    output_forming_function = None,
                                    state_mutator = None)

#### Constructing a Subprocess Based Pipeline Component

    helpers.cons_subprocess_component(process_pipe,
                                      input_forming_function,
                                      output_forming_function,
                                      state_mutator = None)

### Wire Functions

#### Constructing a Function Based Wire

    helpers.cons_wire(schema_conv_function)

#### Constructing a Dictionary Based Wire

    helpers.cons_dictionary_wire(conversions)

#### Wire Up Two Pipeline Components

    helpers.wire_components(component_one, component_two, wire)


