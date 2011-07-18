from aima.core.logic.common import SymbolTerm, AndTerm
from aima.core.logic.propositional.algorithms import KnowledgeBase, WalkSat

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

#
# Example of using WalkSAT algorithm
#

# Number of flips in a single WalkSAT algorithm
NUMBER_OF_FLIPS = 10000
# Probability of flipping symbol's value in a clause
WALK_SAT_PROBABILITY = 0.02
# Number of tries to solve a problem
NUMBER_OF_TRIES = 10

# Create a simple knowledge base from AIMA example
kb = KnowledgeBase()
kb.tell_str("NOT P11")
kb.tell_str("B11 <=> (P12 OR P21)")
kb.tell_str("B21 <=> (P11 OR P22 OR P31)")
kb.tell_str("NOT B11")
kb.tell_str("B21")

# Create sentence with all statements from knowledge base
sentence = kb.as_sentence()

# Create WalkSAT algorithm class
ws = WalkSat()

for i in range(NUMBER_OF_TRIES):
    # Get result model. If solution was found it return Model object, or None otherwise
    result_model = ws.find_model_for(AndTerm(sentence, SymbolTerm("P31")), NUMBER_OF_FLIPS, WALK_SAT_PROBABILITY)
    
    print("Model: " + str(result_model))


