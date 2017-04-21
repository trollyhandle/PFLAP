# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions

from graphics import *
# import DFA

CIR_RADIUS = 20


class State:
    # vars:
    # node - DFANode this State is based on
    # circle - Circle object in the canvas
    # transitions [] - Transitions with this state as source or destination
    # label - Text object in the canvas

    def __init__(self, node):
        self.node = node
        self.circle = Circle(node.center, CIR_RADIUS)
        self.label = Text(node.center, node.name)
        self.transitions = []  # todo ?

    def draw(self, win):
        self.circle.setFill('yellow')
        self.circle.draw(win)
        self.label.draw(win)

    def print(self):
        print("center: ", self.node.center)
        print("circle: ", self.circle)
        print("number of trans: ", len(self.transitions))

    def add_transition(self, line):
        self.transitions.append(line)

    def getCenter(self):
        return self.node.getCenter()

    # if line was clicked
    def tcontains(self, index, click):
        first, second = self.transitions[index].line.getP1(), self.transitions[index].line.getP2()
        return (first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second))

    # move transition
    def move(self, location):
        dx = location.x - self.getCenter().x
        dy = location.y - self.getCenter().y
        self.circle.move(dx, dy)
        self.label.move(dx, dy)

        self.node.center = location

        # update transitions
        for line in self.transitions:

            line.update()



    # delete transition
    def delete(self):
        self.circle.undraw()
        self.label.undraw()
        for i in range(len(self.transitions)):
            self.transitions[i].undraw()
        self.transitions = []

    # redraw transitions - after a move
    def drawAll(self, win):
        for i in range(len(self.transitions)):
            self.transitions[i].line.draw(win)


class Transition:
    # Initialize
    def __init__(self, outState, inState, symbols, line):
        self.line = line
        self.inState = inState
        self.outState = outState
        self.symbols = []
        for i in symbols:
            self.symbols.append(i)
        self.text = None

    # Get first state's center
    def firstCenter(self):
        return self.outState.getCenter()

    # Get second state's center
    def secondCenter(self):
        return self.inState.getCenter()

    # Draw
    def draw(self, win):
        self.line.draw(win)

    # Erase
    def undraw(self):
        self.line.undraw()
        self.text.undraw()

    def update(self):
        pass  # todo

    def drawSymbols(self, win):
        s = ", ".join(self.symbols)
        point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
        textSymbol = Text(point, s)
        textSymbol.draw(win)
        self.text = textSymbol