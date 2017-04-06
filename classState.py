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
    #   transitions : list of transitions going in or out of this state

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

    def contain(self, point):
        return self.circle.contains(point)

    def add_transition(self, line):
        line.setArrow("last")
        self.transitions.append(line)

    def tcontains(self, index, click):
        first, second = self.transitions[index].getP1(), self.transitions[index].getP2()
        return (first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second))

    def erase(self):
        self.circle.undraw()
        for i in range(len(self.transitions)):
            self.transitions[i].undraw()

    """
    # Updates and redraws connected transitions
    def redraw(self, index, new):
        first, second = self.transitions[index].getP1(), self.transitions[index].getP2()
        if (self.circle.contains(first)):
            first = new
        if (self.circle.contains(second)):
            second = new

        toFix = []
        for q in reversed(states):
            if self != q:
                if self.transitions[index] in q.transitions:
                    q.transitions.remove(self.transitions[index])
                    toFix.append(q)

        self.transitions[index].undraw()
        self.transitions[index] = Line(first, second)
        self.transitions[index].setArrow("last")
        for i in range(len(toFix)):
            toFix[i].add_transition(self.transitions[index])
    """

    def drawAll(self, win):
        for i in range(len(self.transitions)):
            self.transitions[i].draw(win)


class States:
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




