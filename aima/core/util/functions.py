from random import randint

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

def select_randomly_from_list(list):
    return list[randint(0, len(list) - 1)]