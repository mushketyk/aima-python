from aima.core.probability.algorithms import ProbabilityDistribution, Query, EnumerationJointAsk

__author__ = 'proger'

import unittest

class ProbabilityDistributionTest(unittest.TestCase):
    def test_probability_of(self):
        pd = ProbabilityDistribution("var1", "var2", "var3")

        pd.set(0.05, False, False, False)
        pd.set(0.01, False, True, False)
        pd.set(0.2, True, True, True)

        expected_probability = 0.06
        result = pd.probability_of({"var3" : False})
        self.assertAlmostEqual(expected_probability, result, places=5)

    def test_set_with_move_values_then_variables(self):
        pd = ProbabilityDistribution("var1", "var2", "var3")

        self.assertRaises(ValueError, pd.set, 0.1, True, False, True, False)

    def test_set_with_less_values_then_variables(self):
        pd = ProbabilityDistribution("var1", "var2", "var3")

        self.assertRaises(ValueError, pd.set, 0.1, True, False)



class EnumerationJointAskTest(unittest.TestCase):
    def test_aima_example(self):
        pd = ProbabilityDistribution("ToothAche", "Cavity", "Catch")

        pd.set(0.108, True, True, True)
        pd.set(0.012, True, True, False)
        pd.set(0.072, False, True, True)
        pd.set(0.008, False, True, False)
        pd.set(0.016, True, False, True)
        pd.set(0.064, True, False, False)
        pd.set(0.144, False, False, True)
        pd.set(0.008, False, False, False)

        q = Query("Cavity", {"ToothAche" : True})

        (true_distr, false_distr) = EnumerationJointAsk().ask(q, pd)
        self.assertAlmostEqual(0.6, true_distr, places=4)
        self.assertAlmostEqual(0.4, false_distr, places=4)

if __name__ == '__main__':
    unittest.main()
