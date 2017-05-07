from collections import deque  # used for generating a DFA

from classState import *

class DFANode:

    def __init__(self, name, center=None, initial=False, final=False):
        self.name = name
        self.transitions = {}  # (character, newstate) k/v pairs
        self.is_final = final
        self.is_initial = initial
        self.center = center  # location of representation in GUI

    def __str__(self):
        t = ', '.join(sorted(['({0} -> {1})'.format(k, v) for k, v in self.transitions.items()]))
        return '"'+self.name+'" -> '+t+(' final'if self.is_final else'')

    def add_transition(self, char, ident):
        # add transition on char to state#ident
        self.transitions[char] = ident

    def get_transition_on(self, char):
        # get the destination state, default -1 if no such transition
        return self.transitions.get(char, -1)

    def get_transition_to(self, dest_state):
        # get
        pass

    def getCenter(self):
        return self.center


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

    def print(self):
        print('initial state id:', self.initial, ' (name: "'+self.nodes[self.initial].name+'")')
        for key in self.nodes.keys():
            print(key, ':', self.nodes[key])

    def simulate(self, input_string, debug=False):
        state = self.initial
        if(debug): print("state {0:2} ({1})".format(state, self.nodes[state].name))
        for char in input_string:
            state = self.nodes[state].get_transition_on(char)
            if (debug): print("state {0:2} ({1})".format(state, self.nodes[state].name))
            if state == -1:
                print('error')
                return
        if self.nodes[state].is_final:
            print('accepted')
        else:
            print('invalid string')

    def inflate(self, win, autolayout=True):
        """
        Creates the graphics representations of this DFA.
        Constructs State objects, and connects with Transition objects based
        on the underlying Node structure.
        Objects are drawn into win.
        :return: list of State objects inflated
        """
        # todo if autolayout, figure out a way to arrange states
        states = []
        state_ids = []
        # construct all State objects
        for k in self.nodes:
            if self.nodes[k].center is None:
                self.nodes[k].center = Point(100, 100)
            s = State(self.nodes[k])
            s.draw(win)
            states.append(s)
            state_ids.append(k)
        for s in states:
            # for each state's OUTGOING transitions:
            for c, t_id in s.node.transitions.items():
                t = Transition(s, states[state_ids[t_id]], c)
                t.draw(win)
                s.add_transition(t)
                states[state_ids[t_id]].add_transition(t)

        return states

    @staticmethod
    def generate(alphabet, transition_fn, initial, accept_fn):
        """
        Generates a DFA algorithmically
        :param alphabet: list of strings in the alphabet
        :param transition_fn: function. accepts state name and transition label.
                                returns new state name
        :param initial: the initial state (string)
        :param accept_fn: function. takes a state, outputs True if it is an accepting state
        :return:
        """
        # make queue for uninitialized states; add initial
        new_states = deque()
        new_states.append(initial)
        ready_states = {initial: 0}
        # make new DFA
        dfa = DFA()
        dfa.nodes[0] = DFANode(initial)
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
                    new_node = DFANode(to_state, final=accept_fn(to_state))
                    dfa.nodes[len(dfa.nodes)] = new_node
                    if accept_fn(to_state):
                        dfa.final.add(new_node)
                # create the transition
                dfa.nodes[ready_states[state]].add_transition(alpha, ready_states[to_state])
        return dfa

    @staticmethod
    def example():
        print('dfa test\n')

        print("Alphabet: { a, b }")
        alphabet = ['a', 'b']

        print("L = { w | len(w) == 3 and w is homogeneous over the alphabet }")
        strlen = 3
        transition_fn = lambda x, a: x+a if len(x) < strlen else x[1:]+a
        accept_fn = lambda x: len(x) == strlen and (x.find('a') == -1 or x.find('b') == -1)

        dfa = DFA.generate(alphabet, transition_fn, '', accept_fn)
        dfa.print()

        dfa.simulate('aaaabbaabbaaa')

        return dfa
