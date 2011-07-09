from aima.core.util.other import PlusInfinity, MinusInfinity

__author__ = 'proger'

import unittest

class PlusInfinityTest(unittest.TestCase):
    def test_greater(self):
        infinity = PlusInfinity()
        self.assertTrue(100 < infinity)
        self.assertTrue(100 <= infinity)
        self.assertTrue(infinity > 100)
        self.assertTrue(infinity >= 100)

    def test_less(self):
        infinity = PlusInfinity()
        self.assertFalse(100 > infinity)
        self.assertFalse(100 >= infinity)
        self.assertFalse(infinity < 100)
        self.assertFalse(infinity <= 100)

    def test_equality(self):
        infinity = PlusInfinity()
        self.assertNotEqual(100, infinity)
        self.assertNotEqual(PlusInfinity(), infinity)

class MinusInfinityTest(unittest.TestCase):
    def test_greater(self):
        infinity = MinusInfinity()
        self.assertTrue(100 > infinity)
        self.assertTrue(100 >= infinity)
        self.assertTrue(infinity < 100)
        self.assertTrue(infinity <= 100)

    def test_less(self):
        infinity = MinusInfinity()
        self.assertFalse(100 < infinity)
        self.assertFalse(100 <= infinity)
        self.assertFalse(infinity > 100)
        self.assertFalse(infinity >= 100)

    def test_equality(self):
        infinity = MinusInfinity()
        self.assertNotEqual(100, infinity)
        self.assertNotEqual(PlusInfinity(), infinity)




if __name__ == '__main__':
    unittest.main()
