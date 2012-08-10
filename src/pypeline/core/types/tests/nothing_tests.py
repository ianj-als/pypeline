import unittest

from pypeline.core.types.nothing import Nothing, return_


class NothingMonadUnitTest(unittest.TestCase):
    def test_bind(self):
        value = 9
        f = lambda a: a * 10
        j = return_(value)
        monad = j >= (lambda a: Just(f(a)))

        self.assertEquals(Nothing(), monad)


    def test_zero(self):
        self.assertFalse(Nothing("nowt"))


    def test_eq(self):
        self.assertTrue(Nothing() == return_("blah"))
        self.assertFalse(Nothing() == None)
        self.assertFalse(Nothing() == object())
