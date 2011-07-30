from random import randint
import random

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

def select_randomly_from_list(list):
    return list[randint(0, len(list) - 1)]

def randbool():
    r = random.random()

    return r > 0.5

def normalize(prob_distr):
    total = sum(prob_distr)
    return map(lambda a: a / total, prob_distr)