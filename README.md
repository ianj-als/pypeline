Pypeline - An arrow based pipelining library 
============================================

A pipeline building library based on *arrows*. Arrows are abstractions of computation, and were proposed by [John Hughes](http://www.cse.chalmers.se/~rjmh/) [Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000]. Like monads, arrows provide a general structure for libraries, but are more general; arrows allow multiple inputs and behaviour that is independed of input.

This implementation is heavily inspired by the Haskell arrow typeclasses: a description of which can be found [here](http://www.haskell.org/arrows/index.html).

Arrow introductory reading:
 * Generalising Monads to Arrows, in Science of Computer Programming 37, pp67-111, May 2000
 * Arrows, By Christoph Galliker, June 2010
 * Kleisli arrows of outrageous fortune, Conor McBride, 2011

Pypeline
--------

This Python implementation provides the following arrows:
 * Function arrow,
 * Function choice arrow, and
 * Kleisli arrow (It is expected that the Kleisli choice arrow will be implemented shortly).

And also provides helper functions that lift the arrow abstraction to a *pipeline component* level, in order that pipelines can be constructed without "seeing" and arrow directly. However, if the programmer wishes the underlying arrow classes can be used to build pipelines using the helper function.
