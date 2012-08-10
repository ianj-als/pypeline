import unittest

from pypeline.core.types.either import Either, Left, Right


class EitherUnitTests(unittest.TestCase):
    def test_eq(self):
        self.assertEquals(Left(10), Left(10))
        self.assertEquals(Right("something"), Right("something"))
        self.assertNotEquals(Left(10), Right(10))
