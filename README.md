Pypeline - An arrow based pipelining library 
============================================

Pypeline is licensed using the [Lesser GNU Public License Version 3](http://www.gnu.org/licenses/lgpl.txt).

A pipeline building library based on *arrows*. Arrows are abstractions of computation, and were proposed by [John Hughes](http://www.cse.chalmers.se/~rjmh/) [Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000]. Like monads, arrows provide a general structure for libraries, but are more general; arrows allow multiple inputs and behaviour that is independed of input.

This implementation is heavily inspired by the Haskell arrow typeclasses: a description of which can be found [here](http://www.haskell.org/arrows/index.html).

Arrow introductory reading:
 * Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000
 * Arrows, By Christoph Galliker, June 2010
 * Kleisli arrows of outrageous fortune, Conor McBride, 2011

Installation
------------

setuptools is required to build, test and install Pypeline. Eggs can be built and installed also.

To install an Egg:

  `sudo python setup.py install bdist_egg`

To view setup help:

  `python setup.py --help`

Implementation
--------------

This Python implementation provides the following arrows:
 * Function arrow,
 * Function choice arrow, and
 * Kleisli arrow (It is expected that the Kleisli choice arrow will be implemented shortly).

And also provides helper functions that lift the arrow abstraction to a *pipeline component* level, in order that pipelines can be constructed without "seeing" and arrow directly. However, if the programmer wishes, the underlying arrow classes can be used to build pipelines with or without the helper functions.

The library also implements some monad classes, primarily, for use with the Kleisli arrow class. These are:
 * Maybe, and
 * State.

Pipelines
---------

Pipelines can be constructed using the helpers function in the [pypeline.helpers.helpers](https://github.com/ianj-als/pypeline/blob/master/src/pypeline/helpers/helpers.py) module. There are three primatives that can be constructed:
 1. Pipelines,
 2. Pipeline components, and
 3. Wires.
