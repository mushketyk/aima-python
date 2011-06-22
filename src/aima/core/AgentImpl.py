from aima.core.Agent import Action

__author__ = 'Ivan Mushketik'

class CutOffIndicatorAction(Action):
    def is_noop(self):
        return True

    def __eq__(self, other):
        return isinstance(other, CutOffIndicatorAction)


class NoOpAction(Action):
    def is_noop(self):
        return True

    def __eq__(self, other):
        return isinstance(other, NoOpAction)