from aima.core.probability.algorithms import ProbabilityDistribution, Query, EnumerationJointAsk, BayesNetNode, BayesNet, EnumerationAsk, Randomizer

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

    def test_is_true_for_root_node(self):
        root_node = BayesNetNode("Cloudy")

        root_node.set_probablity(0.9, [True])

        self.assertTrue(root_node.is_true_for(0.4, {}))
        self.assertFalse(root_node.is_true_for(0.99, {}))

    def test_is_true_for_not_root_node(self):
        sprinkler_node = BayesNetNode("Sprinkler")
        rain_node = BayesNetNode("Rain")

        wet_grass_node = BayesNetNode("WetGrass")
        wet_grass_node.influenced_by(sprinkler_node, rain_node)

        wet_grass_node.set_probablity(0.99, [True, True])
        wet_grass_node.set_probablity(0.90, [True, False])
        wet_grass_node.set_probablity(0.90, [False, True])
        wet_grass_node.set_probablity(0, [False, False])

        self.assertTrue(wet_grass_node.is_true_for(0.5, {"Sprinkler" : True, "Rain" : True}))
        self.assertFalse(wet_grass_node.is_true_for(0.99876, {"Sprinkler" : True, "Rain" : True}))

def create_burglary_network():
    burglary = BayesNetNode("Burglary")
    earthQuake = BayesNetNode("EarthQuake")
    alarm = BayesNetNode("Alarm")
    johnCalls = BayesNetNode("JohnCalls")
    maryCalls = BayesNetNode("MaryCalls")

    alarm.influenced_by(burglary, earthQuake)
    johnCalls.influenced_by(alarm)
    maryCalls.influenced_by(alarm)

    burglary.set_probablity(0.001, [True])
    earthQuake.set_probablity(0.002, [True])

    alarm.set_probablity(0.95, [True, True])
    alarm.set_probablity(0.94, [True, False])
    alarm.set_probablity(0.29, [False, True])
    alarm.set_probablity(0.001, [False, False])

    johnCalls.set_probablity(0.9, [True])
    johnCalls.set_probablity(0.05, [False])

    maryCalls.set_probablity(0.7, [True])
    maryCalls.set_probablity(0.01, [False])

    return BayesNet((burglary, earthQuake))

class BayesNetTest(unittest.TestCase):
    def test_get_root_variable(self):
        root_node = BayesNetNode("root")
        bn = BayesNet([root_node])

        vars = bn.get_variables()
        self.assertSameElements(["root"], vars)

    def test_get_variables_with_several_childs(self):
        root_node = BayesNetNode("root")
        child1 = BayesNetNode("child1")
        child2 = BayesNetNode("child2")
        child3 = BayesNetNode("child3")

        child1.influenced_by(root_node)
        child2.influenced_by(root_node)
        child3.influenced_by(root_node)

        bn = BayesNet([root_node])

        vars = bn.get_variables()
        self.assertSameElements(["root", "child1", "child2", "child3"], vars)

    def test_get_variables_with_several_roots(self):
        root_node1 = BayesNetNode("root1")
        root_node2 = BayesNetNode("root2")

        child1 = BayesNetNode("child1")
        child2 = BayesNetNode("child2")
        child3 = BayesNetNode("child3")

        child1.influenced_by(root_node1)
        child2.influenced_by(root_node1, root_node2)
        child3.influenced_by(root_node2)

        bn = BayesNet([root_node1, root_node2])

        vars = bn.get_variables()
        self.assertSameElements(["root1", "root2", "child1", "child2", "child3"], vars)


    def test_variables_obtained_from_burglary_network(self):
        net = create_burglary_network()
        vars = net.get_variables()
        self.assertSameElements(["Burglary", "EarthQuake", "Alarm", "JohnCalls", "MaryCalls"], vars)

    def test_probability_of_root_node(self):
        net = create_burglary_network()

        true_probability = net.probability_of("Burglary", True, dict())
        self.assertAlmostEqual(0.001, true_probability, places=5)

        false_probability = net.probability_of("Burglary", False, dict())
        self.assertAlmostEqual(0.999, false_probability, places=5)

    def test_probability_of_not_root_node(self):
        net = create_burglary_network()

        prob = net.probability_of("Alarm", True, {"Burglary" : True, "EarthQuake" : True})
        self.assertAlmostEqual(0.95, prob)

        prob = net.probability_of("Alarm", False, {"Burglary" : True, "EarthQuake" : True})
        self.assertAlmostEqual(0.05, prob)

class EnumerationAskTest(unittest.TestCase):
    def test_enumerateion_ask_aima_example(self):
        query = Query("Burglary", {"JohnCalls" : True, "MaryCalls" : True})

        true_probability, false_probability = EnumerationAsk().ask(query, create_burglary_network())

        self.assertAlmostEqual(true_probability, 0.284, places=3)
        self.assertAlmostEqual(false_probability, 0.716, places=3)

    def test_enumeration_all_variables_excluding_query_known(self):
        query = Query("Alarm", {"Burglary" : False, "EarthQuake" : False, "JohnCalls" : True, "MaryCalls" : True})

        true_probability, false_probability = EnumerationAsk().ask(query, create_burglary_network())

        self.assertAlmostEqual(true_probability, 0.557, places=2)
        self.assertAlmostEqual(false_probability, 0.442, places=3)

class MockRandomizer(Randomizer):
    def __init__(self, values):
        self.values = values
        self.curr = 0

    def next_double(self):
        if self.curr == len(self.values):
            self.curr = 0

        value = self.values[self.curr]
        self.curr += 1
        return value

class ApproximateInference(unittest.TestCase):
    def test_prior_sample(self):
        net = self._create_wet_grass_network()
        randomizer = MockRandomizer([0.5, 0.5, 0.5, 0.5])

        table = net.get_prior_sample(randomizer)

        self.assertTrue(table["Cloudy"])
        self.assertFalse(table["Sprinkler"])
        self.assertTrue(table["Rain"])
        self.assertTrue(table["WetGrass"])

    def test_rejection_sample(self):
        net = self._create_wet_grass_network()
        randomizer = MockRandomizer([0.1])

        evidence = {"Sprinkler" : True}

        (true_probability, false_probability) = net.rejection_sample("Rain", evidence, 100, randomizer)
        self.assertAlmostEqual(1, true_probability)
        self.assertAlmostEqual(0, false_probability)

    def test_likelihood_weighting(self):
        randomizer = MockRandomizer([0.5, 0.5, 0.5, 0.5])

        net = self._create_wet_grass_network()
        evidence = {"Sprinkler" : True}
        (true_probability, false_probability) = net.likelihood_weighting("Rain", evidence, 1000, randomizer)

        self.assertAlmostEqual(1, true_probability)
        self.assertAlmostEqual(0, false_probability)

    def test_mcmc_ask(self):
        net = self._create_wet_grass_network()
        randomizer = MockRandomizer([0.5, 0.5, 0.5, 0.5])

        evidence = {"Sprinkler" : True}
        true_probability, false_probability = net.mcmc_ask("Rain", evidence, 1, randomizer)

        self.assertAlmostEqual(0.333, true_probability, places=3)
        self.assertAlmostEqual(0.666, false_probability, places=2)

    def _create_wet_grass_network(self):
        cloudy_node = BayesNetNode("Cloudy")
        sprinkler_node = BayesNetNode("Sprinkler")
        rain_node = BayesNetNode("Rain")
        wet_grass_node = BayesNetNode("WetGrass")

        sprinkler_node.influenced_by(cloudy_node)
        rain_node.influenced_by(cloudy_node)
        wet_grass_node.influenced_by(rain_node, sprinkler_node)

        cloudy_node.set_probablity(0.5, [True])

        sprinkler_node.set_probablity(0.1, [True])
        sprinkler_node.set_probablity(0.5, [False])

        rain_node.set_probablity(0.8, [True])
        rain_node.set_probablity(0.2, [False])

        wet_grass_node.set_probablity(0.99, [True, True])
        wet_grass_node.set_probablity(0.9, [True, False])
        wet_grass_node.set_probablity(0.9, [False, True])
        wet_grass_node.set_probablity(0, [False, False])

        return BayesNet([cloudy_node])




if __name__ == '__main__':
    unittest.main()
