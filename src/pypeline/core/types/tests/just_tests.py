import unittest

from pypeline.core.types.just import Just, return_


class JustMonadUnitTest(unittest.TestCase):
    def test_bind(self):
        value = 9
        f = lambda a: a * 10
        j = return_(value)
        monad = j >= (lambda a: Just(f(a)))

        self.assertEquals(Just(f(value)), monad)


    def test_zero(self):
        self.assertTrue(return_(False))
        self.assertTrue(return_(0))
        self.assertTrue(return_(""))
        self.assertTrue(return_(list()))
        self.assertTrue(return_(dict()))


    def test_eq(self):
        self.assertTrue(Just(10) == return_(10))
        self.assertFalse(Just(10) == None)
        self.assertFalse(Just(10) == object())
