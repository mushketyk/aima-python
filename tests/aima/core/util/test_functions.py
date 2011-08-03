from aima.core.util.functions import rest

__author__ = 'proger'

import unittest

class RestTest(unittest.TestCase):
    def test_many_elements_rest(self):
        l = [1, 2, 3]
        rst = rest(l)
        self.assertSequenceEqual([2, 3], rst)

    def test_single_element_rest(self):
        l = [1]
        rst = rest(l)
        self.assertSequenceEqual([], rst)

    def test_no_elements_rest(self):
        l = []
        rst = rest(l)
        self.assertSequenceEqual([], rst)

if __name__ == '__main__':
    unittest.main()
