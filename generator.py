"""
File containing DFA-generating code
Required elements:
    alphabet - list of characters used
    inital - first state name
    transition - function: accepts a state and input, outputs new state
    accept - function: takes a state, outputs True if state is final
"""

strlen = 3
alphabet = ['a', 'b']

initial = ""

def transition(x, a):
    if len(x) < strlen:
        return x + a
    else:
        return x[1:] + a


def accept(x):
    # meets min length and is homogenous
    return len(x) == strlen and (x.find('a') == -1 or x.find('b') == -1)
