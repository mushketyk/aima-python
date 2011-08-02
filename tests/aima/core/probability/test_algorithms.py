from aima.core.probability.algorithms import ProbabilityDistribution, Query, EnumerationJointAsk, BayesNetNode

__author__ = 'proger'

import unittest

class ProbabilityDistributionTest(unittest.TestCase):
    def test_probability_of(self):
        pd = ProbabilityDistribution(("var1", "var2", "var3"))

        pd.set(0.05, (False, False, False))
        pd.set(0.01, (False, True, False))
        pd.set(0.2, (True, True, True))

        expected_probability = 0.06
        result = pd.probability_of({"var3" : False})
        self.assertAlmostEqual(expected_probability, result, places=5)

    def test_set_with_move_values_then_variables(self):
        pd = ProbabilityDistribution(("var1", "var2", "var3"))

        self.assertRaises(ValueError, pd.set, 0.1, (True, False, True, False))

    def test_set_with_less_values_then_variables(self):
        pd = ProbabilityDistribution(("var1", "var2", "var3"))

        self.assertRaises(ValueError, pd.set, 0.1, (True, False))



class EnumerationJointAskTest(unittest.TestCase):
    def test_aima_example(self):
        pd = ProbabilityDistribution(("ToothAche", "Cavity", "Catch"))

        pd.set(0.108, (True, True, True))
        pd.set(0.012, (True, True, False))
        pd.set(0.072, (False, True, True))
        pd.set(0.008, (False, True, False))
        pd.set(0.016, (True, False, True))
        pd.set(0.064, (True, False, False))
        pd.set(0.144, (False, False, True))
        pd.set(0.008, (False, False, False))

        q = Query("Cavity", {"ToothAche" : True})

        (true_distr, false_distr) = EnumerationJointAsk().ask(q, pd)
        self.assertAlmostEqual(0.6, true_distr, places=4)
        self.assertAlmostEqual(0.4, false_distr, places=4)

class BayesNetNodeTest(unittest.TestCase):
    def test_probability_of_root_variable(self):
        bnn = BayesNetNode("var1")
        bnn.set_probablity(0.3, [True])

        false_result = bnn.probability_of({"var1": False})
        expected_false_result = 0.7
        self.assertAlmostEqual(expected_false_result, false_result, places=5)

        true_result = bnn.probability_of({"var1": True})
        expected_true_result = 0.3
        self.assertAlmostEqual(expected_true_result, true_result, places=5)

    def test_childs(self):
        root_node = BayesNetNode("root")

        child1 = BayesNetNode("child1")
        child2 = BayesNetNode("child2")
        child3 = BayesNetNode("child3")

        child1.influenced_by(root_node)
        child2.influenced_by(root_node)
        child3.influenced_by(root_node)

        self.assertSameElements([child1, child2, child3], root_node.children)

    def test_parents(self):
        root1 = BayesNetNode("root1")
        root2 = BayesNetNode("root2")
        root3 = BayesNetNode("root3")

        child = BayesNetNode("child")
        child.influenced_by(root1)
        child.influenced_by(root2)
        child.influenced_by(root3)

        self.assertSameElements([root1, root2, root3], child.parents)

    def test_probability_of_non_root_var(self):
        root_bnn1 = BayesNetNode("root1")
        root_bnn2 = BayesNetNode("root2")
        root_bnn3 = BayesNetNode("root3")

        dependent_bnn = BayesNetNode("dependentNode")
        dependent_bnn.influenced_by(root_bnn1, root_bnn2, root_bnn3)

        dependent_bnn.influenced_by(root_bnn1, root_bnn2, root_bnn3)

        dependent_bnn.set_probablity(0.1, (True, True, True))
        dependent_bnn.set_probablity(0.15, (True, False, True))
        dependent_bnn.set_probablity(0.2, (True, True, False))
        dependent_bnn.set_probablity(0.25, (False, True, True))
        dependent_bnn.set_probablity(0.3, (False, False, True))

        result = dependent_bnn.probability_of({"root1" : True})
        expected_result = 0.1 + 0.15 + 0.2

        self.assertAlmostEqual(expected_result, result, places=5)



if __name__ == '__main__':
    unittest.main()
