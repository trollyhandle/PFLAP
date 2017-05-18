from collections import deque  # used for generating a DFA

from classState import *


class DFANode:

    def __init__(self, name, center=None, initial=False, final=False, id=-1):
        self.id = id
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
        self.free_ids = set()

    def __str__(self):
        return 'DFA containing {0} nodes'.format(len(self.nodes))

    def get_node_by_id(self, ident):
        return self.nodes.get(ident, None)

    def add_node(self, node):
        id = node.id
        if id < 0:
            id = self.get_free_id()
            node.id = id
        if id in self.nodes:
            return False
        self.nodes[id] = node
        return True

    def remove_node(self, node):
        print('removing node', node)
        if node.id in self.nodes:
            self.nodes.pop(node.id)
            self.free_ids.add(node.id)
            # todo transitions to/from node

    def get_free_id(self):
        f = len(self.nodes)
        if len(self.free_ids) > 0: f = self.free_ids.pop()
        return f

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
                print('simulation error')
                return
        if self.nodes[state].is_final:
            print('string accepted')
        else:
            print('string not accepted')

    def inflate(self, win, vertical_offset):
        """
        Creates the graphics representations of this DFA.
        Constructs State objects, and connects with Transition objects based
        on the underlying Node structure.
        Objects are drawn into win.
        :return: list of State objects inflated
        """
        def layout(num_nodes, win_padding=60):
            aspect_ratio = (win.getWidth() - 2 * win_padding)\
                           / (win.getHeight() - 2 * win_padding - vertical_offset)
            nodes_tall = int(math.sqrt(num_nodes/aspect_ratio))
            nodes_wide = int(num_nodes / nodes_tall)
            hspace = (win.getWidth() - 2 * win_padding) // nodes_wide
            vspace = (win.getHeight() - 2 * win_padding) // nodes_tall
            for j in range(nodes_tall + 1):
                for i in range(nodes_wide + 1):
                    x = win_padding + i * hspace
                    y = vertical_offset + win_padding + j * vspace + (i%2)*(vspace//4)
                    yield Point(x, y)
            while True: yield Point(50, vertical_offset+50)  # in case of overflow
        position_generator = layout(len(self.nodes))

        states = []
        state_ids = []
        # construct all State objects
        for k in self.nodes:
            if self.nodes[k].center is None:
                self.nodes[k].center = next(position_generator)
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
    def generate(alphabet, transition_fn, first_state, accept_fn):
        """
        Generates a DFA algorithmically
        :param alphabet: list of strings in the alphabet
        :param transition_fn: function. accepts state name and transition label.
                                returns new state name
        :param first_state: the initial state (string)
        :param accept_fn: function. takes a state, outputs True if it is an accepting state
        :return:
        """
        # make queue for uninitialized states; add initial
        new_states = deque()
        new_states.append(first_state)
        ready_states = {first_state: 0}
        # make new DFA
        dfa = DFA()
        name = 'λ' if len(first_state) == 0 else first_state
        dfa.nodes[0] = DFANode(name, initial=True, final=accept_fn(first_state), id=0)
        dfa.initial = 0
        # for each state in q:
        while len(new_states) > 0:
            state = new_states.popleft()
            for alpha in alphabet:
                to_state = transition_fn(state, alpha)
                if to_state not in ready_states:
                    # trace a new state, add to DFA
                    new_states.append(to_state)
                    node_id = len(dfa.nodes)
                    name = 'λ' if len(to_state) == 0 else to_state
                    ready_states[to_state] = node_id
                    new_node = DFANode(name, final=accept_fn(to_state), id=node_id)
                    dfa.nodes[node_id] = new_node
                    if accept_fn(to_state):
                        dfa.final.add(new_node)
                # create the transition
                dfa.nodes[ready_states[state]].add_transition(alpha, ready_states[to_state])
        return dfa

    @staticmethod
    def load():
        import generator as g
        return DFA.generate(g.alphabet, g.transition, g.initial, g.accept)
