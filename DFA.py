import json
import classState as State
from graphics import *

# combine this class with State?
class Node:
    # vars
    # state_object - State graphically representing this node
    # transitions - list of outward transitions
    #   transition list - (dest, value) pairs
    # id - identifier for this state. not the same as state name
    def __init__(self, id, gui=None):
        self.id = id
        self.state_object = gui
        self.transitions = {}

    # add transition from this node to dest node
    def add_transition_to(self, dest, transit):
        self.transitions[transit] = dest.id

    # assign a State object to this node
    def set_graphic(self, gui):
        self.state_object = gui

    def has_graphic(self):
        return self.state_object is not None


class NodeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if o.has_graphic():
            return [o.id, o.state_object.name, o.transitions]
        else:
            return [o.id, None, o.transitions]


class DFA:
    # vars
    # node_list - list of all nodes in this DFA
    #
    def __init__(self):
        self.node_list = []

    def __str__(self):
        return ''

    def add_node(self):
        pass


def main():
    print('dfa test')

    dfa = {}
    dfa[0] = Node(0)
    dfa[0].add_transition_to(Node(1), 'x')
    dfa[0].set_graphic(State.State(Point(0,0), [], None, 'test'))

    test = json.dumps(dfa[0], cls=NodeJSONEncoder)
    print(test)


    # with open('trans_ll.txt') as f:
    #     for line in f.readlines():
    #         Node.construct(line.strip())
    #         print()




main()