import json
from collections import deque
from graphics import *


class State:

    def __init__(self, name, is_final=False):
        self.name = name
        self.transitions = []
        self.final = is_final

    def __str__(self):
        return '"'+self.name+'" -> '+str(self.transitions)+(' final'if self.final else'')

    def add_transition(self, char, ident):
        # add transition on char to state#ident
        self.transitions.append((char, ident))

    def dump(self):
        class StateEncoder(json.JSONEncoder):
            def default(self, o):
                if o.has_graphic():
                    return [o.id, o.state_object.name, o.transitions]
                else:
                    return [o.id, None, o.transitions]
        return json.dumps(self, cls=StateEncoder)


class DFA:
    # vars
    # nodes {} - dict of nodes in this dfa
    # initial - initial node of the FA
    # final {} - set of final/accepting nodes in the dfa

    def __init__(self):
        self.nodes = {}
        self.initial = None
        self.final = set()

    def __str__(self):
        return 'DFA containing {0} nodes'.format(len(self.nodes))

    def get_node_by_id(self, ident):
        return self.nodes[ident]

    def dumps(self):
        class DFAEncoder(json.JSONEncoder):
            def default(self, o):
                return [o.get_node_by_id(key) for key in o.nodes ]
        return json.dumps(self, cls=DFAEncoder)

    def print(self):
        print('initial state id:', self.initial, ' (name: "'+self.nodes[self.initial].name+'")')
        for key in self.nodes.keys():
            print(key, ':', self.nodes[key])

    @staticmethod
    def generate(alphabet, transition_fn, initial, accept_fn):
        # make queue for uninitialized states; add initial
        new_states = deque()
        new_states.append(initial)
        ready_states = {initial: 0}
        # make new DFA
        dfa = DFA()
        dfa.nodes[0] = State(initial)
        dfa.initial = 0
        # for each state in q:
        while len(new_states) > 0:
            state = new_states.popleft()
            for alpha in alphabet:
                to_state = transition_fn(state, alpha)
                if to_state not in ready_states:
                    # trace a new state, add to DFA
                    new_states.append(to_state)
                    ready_states[to_state] = len(dfa.nodes)
                    dfa.nodes[len(dfa.nodes)] = State(to_state, is_final=accept_fn(to_state))
                # create the transition
                dfa.nodes[ready_states[state]].add_transition(alpha, ready_states[to_state])
        return dfa


def main():
    print('dfa test\n')

    alphabet = ['a', 'b']
    strlen = 3
    transition_fn = lambda x, a: x+a if len(x) < strlen else x[1:]+a
    accept_fn = lambda x: len(x) == strlen and (x.find('a') == -1 or x.find('b') == -1)
    dfa = DFA.generate(alphabet, transition_fn, '', accept_fn)
    dfa.print()
    # dfa[0] = State(0)
    # dfa[0].add_transition_to(State(1), 'x')
    # dfa[0].set_graphic(State.State(Point(0,0), [], None, 'test'))

    # test = dfa.dumps()
    # print(test)

    # with open('trans_ll.txt') as f:
    #     for line in f.readlines():
    #         Node.construct(line.strip())
    #         print()


main()