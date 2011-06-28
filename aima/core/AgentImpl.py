from aima.core.Agent import Action

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'


class CutOffIndicatorAction(Action):
    def __init__(self):
        super().__init__("CufOff")

    def is_noop(self):
        return True

    def __eq__(self, other):
        return isinstance(other, CutOffIndicatorAction)


class NoOpAction(Action):
    def __init__(self):
        super().__init__("NoOp")

    def is_noop(self):
        return True

    def __eq__(self, other):
        return isinstance(other, NoOpAction)

