from aima.core.search.csp import Variable, Domain, Assignment, BacktrackingStrategy, MapCSP, CSP, NotEqualConstraint, Inference, ImprovedBacktrackingStrategy, Selection

__author__ = 'proger'

import unittest

class VariableTest(unittest.TestCase):
    def test_equality(self):
        var1 = Variable("var1")
        var1_2 = Variable("var1")
        var2 = Variable("var2")

        self.assertEqual(var1, var1_2)
        self.assertNotEquals(var1, var2)

class DomainTest(unittest.TestCase):
    def setUp(self):
        self.domain = Domain([1, 2, 3, 4])

    def test_size(self):
        self.assertEqual(4, self.domain.size())

    def test_get(self):
        self.assertEqual(1, self.domain.get(0))
        self.assertEqual(4, self.domain.get(3))

    def test_is_empty(self):
        self.assertFalse(self.domain.is_empty())
        
        empty_domain = Domain([])
        self.assertTrue(empty_domain.is_empty())

    def test_contains(self):
        self.assertTrue(self.domain.contains(2))
        self.assertFalse(self.domain.contains(42))

    def test_iter(self):
        lst = list(self.domain)
        self.assertListEqual([1, 2, 3, 4], lst)

    def test_equals(self):
        self.assertEquals(self.domain, Domain([1, 2, 3, 4]))
        self.assertNotEquals(self.domain, Domain((10, 20, 30, 42)))
        self.assertNotEquals(self.domain, [1, 2, 3, 4])


class AssignmentTest(unittest.TestCase):
    var1 = Variable("var1")
    var2 = Variable("var2")

    def test_get_variables(self):
        assignment = Assignment()
        self.assertEqual(0, len(assignment.get_variables()))

        assignment.set_assignment(self.var1, 1)
        assignment.set_assignment(self.var2, 2)
        self.assertSameElements([self.var1, self.var2], assignment.get_variables())

    def test_get_assignment(self):
        assignment = Assignment()
        assignment.set_assignment(self.var1, 1)

        self.assertEqual(1, assignment.get_assignment(self.var1))
        self.assertEqual(None, assignment.get_assignment(self.var2))

    def test_is_complete(self):
        vars = [self.var1, self.var2]
        assignment = Assignment()
        assignment.set_assignment(self.var1, 1)

        self.assertFalse(assignment.is_complete(vars))

        assignment.set_assignment(self.var2, 2)
        self.assertTrue(assignment.is_complete(vars))


class BacktrackingSearchTest(unittest.TestCase):
    def test_search(self):
        bs = BacktrackingStrategy()
        map_csp = MapCSP()

        result = bs.solve(map_csp)
        self.assertEquals(MapCSP.GREEN, result.get_assignment(MapCSP.WA))
        self.assertEquals(MapCSP.RED, result.get_assignment(MapCSP.NT))
        self.assertEquals(MapCSP.BLUE, result.get_assignment(MapCSP.SA))
        self.assertEquals(MapCSP.GREEN, result.get_assignment(MapCSP.Q))
        self.assertEquals(MapCSP.RED, result.get_assignment(MapCSP.NSW))
        self.assertEquals(MapCSP.GREEN, result.get_assignment(MapCSP.V))
        self.assertEquals(MapCSP.RED, result.get_assignment(MapCSP.T))

    def test_search_failed(self):
        var1 = Variable('var1')
        var2 = Variable('var2')
        domain = Domain(['v1'])

        bs = BacktrackingStrategy()
        csp = CSP([var1, var2])

        csp.add_constraint(NotEqualConstraint(var1, var2))
        csp.set_domain(var1, domain)
        csp.set_domain(var2, domain)

        result = bs.solve(csp)
        self.assertEquals(None, result)

if __name__ == '__main__':
    unittest.main()
