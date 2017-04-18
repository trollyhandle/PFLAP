# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions


from graphics import *


class State:
    # Class variables:
    #   circle : the circle object graphically representing this state
    #   start : (bool) this state is a starting state (initial tracked by FA)
    #   final : (bool) this state is an accepting state (initial tracked by FA)
    #   center : Point(x, y) of which the state is centered
    #   name : the name for this state. defaults to q0, q1, ... qn
    #   label : textbox displaying name of state on circle
    #   transitions_in[] : list of transitions going in or out of this state
    #   transitions_out[] : list of transitions going to this state

    def __init__(self, center, transitions, circle, name):
        self.final = False
        self.start = False
        self.center = center
        self.transitions = transitions
        self.circle = circle
        self.name = name
        self.label = Text(center, name)

    def print(self):
        print("center: ", self.center)
        print("circle: ", self.circle)
        print("number of trans: ", len(self.transitions))

    def add_transition(self, line):
        self.transitions.append(line)

    def tcontains(self, index, click):
        first, second = self.transitions[index].line.getP1(), self.transitions[index].line.getP2()
        return (first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second))

    def erase(self, win):
        self.circle.undraw()
        self.label.undraw()
        for i in range(len(self.transitions)):
            self.transitions[i].undraw(win)
        self.transitions = []

    def drawAll(self, win):
        for i in range(len(self.transitions)):
            self.transitions[i].line.draw(win)
            #self.transitions[i].text.draw(win)

class Transition:
    # Initialize
    def __init__(self, outState, inState, symbols, line):
        self.line = line
        self.inState = inState
        self.outState = outState
        self.symbols = []
        for i in symbols:
            self.symbols.append(i)
        self.text = ""

    # Get first state's center
    def firstCenter(self):
        return self.outState.center

    # Get second state's center
    def secondCenter(self):
        return self.inState.center

    # Draw
    def draw(self, win):
        self.line.draw(win)

    # Erase
    def undraw(self, win):
        self.line.undraw()
        self.text.undraw()

    def drawSymobls(self, win):
        s = ""
        for i in range(len(self.symbols)):
            if i == len(self.symbols) - 1:
                s += self.symbols[i]
            else:
                s += self.symbols[i] + ", "
        point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
        textSymbol = Text(point, s)
        textSymbol.draw(win)
        self.text = textSymbol


