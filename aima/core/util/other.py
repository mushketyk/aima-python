__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class Comparator:
    """
        Comparator for comparing to elements.
    """
    def compare(self, first, second):
        """
            Compare two elements

            return(int) > 0 if second element is larger, < 0 if first element is larger, 0 if elements are equal
        """
        pass


class Infinity:
        def __gt__(self, other):
            return True

        def __ge__(self, other):
            return True

        def __lt__(self, other):
            return False

        def __le__(self, other):
            return False

        def __eq__(self, other):
            return False