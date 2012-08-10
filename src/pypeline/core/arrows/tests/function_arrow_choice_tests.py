import unittest

from pypeline.core.arrows.function_arrow import FunctionArrow
from pypeline.core.arrows.function_arrow_choice import FunctionArrowChoice, test, if_maker
from pypeline.core.types.either import Left, Right


class ArrowChoiceUnitTests(unittest.TestCase):
    # Left
    def test_left(self):
        f = lambda x: x + 1
        arrow = FunctionArrowChoice(f).left()
        value = 7
        self.assertEquals(Left(f(value)), arrow(Left(value)))
        self.assertEquals(Right(value), arrow(Right(value)))


    # Right
    def test_right(self):
        f = lambda x: x + 1
        arrow = FunctionArrowChoice(f).right()
        value = 7
        self.assertEquals(Left(value), arrow(Left(value)))
        self.assertEquals(Right(f(value)), arrow(Right(value)))


    # (+++) : Split
    def test_split(self):
        f = lambda x: x + 1
        g = lambda x: x * 2
        arrow = FunctionArrowChoice(f) + FunctionArrowChoice(g)
        value = 7
        self.assertEquals(Left(f(value)), arrow(Left(value)))
        self.assertEquals(Right(g(value)), arrow(Right(value)))


    # (|||) : Fanin
    def test_fanin(self):
        f = lambda x: x + 1
        g = lambda x: x * 2
        arrow = FunctionArrowChoice(f) | FunctionArrowChoice(g)
        value = 7
        self.assertEquals(f(value), arrow(Left(value)))
        self.assertEquals(g(value), arrow(Right(value)))


    # Test the value of the input to an arrow
    def test_test(self):
        a = lambda x: x % 2
        arrow = FunctionArrow(a)
        test_arrow = test(arrow)
        for value in range(0, 9):
            target = Left(value) if a(value) else Right(value)
            self.assertEquals(target, test_arrow(value))
