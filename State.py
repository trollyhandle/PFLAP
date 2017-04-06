# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions

from graphics import Circle


class State:
    gui_size = 20

    # Class variables:
    #   circ : the circle object graphically representing this state
    #   final : (bool) this state is an accepting state (initial tracked by FA)
    #
    #   name: the name for this state. defaults to q0, q1, ... qn
    #   labels[]: list of labels for this state. no effect on DFA
    #   trans_in[] : list of transitions originating from this state
    #   trans_out[] : list of transitions leading to this state

    def __init__(self, centerpoint):
        self.circ = Circle(centerpoint, self.gui_size)
        self.transitions = []
        self.final = False

    def __str__(self):
        pass




