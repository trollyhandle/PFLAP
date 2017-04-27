# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions

from graphics import *
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
        #: :type: list of Transition
        self.transitions = []  # todo list or dict?

    def draw(self, win):
        self.circle.setFill('yellow')
        self.circle.draw(win)
        self.label.draw(win)

    # Draw state and transition(s)
    def drawAll(self, win):
        self.draw(win)
        # Update transitions
        for line in self.transitions:
            line.draw(win)

    def print(self):
        print("center: ", self.node.center)
        print("circle: ", self.circle)
        print("number of trans: ", len(self.transitions))

    def add_transition(self, line):
        self.transitions.append(line)

    def remove_transition(self, line):
        if line in self.transitions:
            self.transitions.remove(line)

    def getCenter(self):
        return self.node.getCenter()

    # If transition line was clicked
    def tcontains(self, index, click):
        first, second = self.transitions[index].line.getP1(), self.transitions[index].line.getP2()
        return first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second)

    # Move transition
    def move(self, location, win):
        dx = location.x - self.getCenter().x
        dy = location.y - self.getCenter().y
        self.circle.move(dx, dy)
        self.label.move(dx, dy)

        self.node.center = location

        # Update transitions
        for line in self.transitions:
            line.draw(win)

    # Delete state and all of its transitions
    def delete(self):
        self.circle.undraw()
        self.label.undraw()
        for i in range(len(self.transitions)-1, -1, -1):
            self.transitions[i].remove()
        self.transitions = []


class Transition:
    # vars:
    # outState - State at tail of transition
    # inState - State at head of transition
    # symbols - Transition symbols

    def __init__(self, outState, inState, symbols):
        #: :type: State
        self.inState = inState
        #: :type: State
        self.outState = outState
        self.symbols = []
        for i in symbols:
            self.symbols.append(i)
        self.line = None
        self.text = None

    # Get first state's center
    def firstCenter(self):
        return self.outState.getCenter()

    # Get second state's center
    def secondCenter(self):
        return self.inState.getCenter()

    # Draw
    def draw(self, win):
        if self.line is not None:
            self.line.undraw()
            self.text.undraw()
        line_first = self.movePoints(self.firstCenter(), self.secondCenter())
        line_second = self.movePoints(self.secondCenter(), self.firstCenter())
        self.line = Line(line_first, line_second)
        self.line.setArrow("last")
        self.line.draw(win)

        s = ", ".join(self.symbols)
        point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
        self.text = Text(point, s)
        self.text.draw(win)

    # Erase
    def undraw(self):
        self.line.undraw()
        self.text.undraw()

    def remove(self):
        self.undraw()
        self.outState.remove_transition(self)
        self.inState.remove_transition(self)

    def movePoints(self, first, second):
        """
        Takes two points and returns a point that is distance t from first point
        """
        d = math.sqrt(((second.getX() - first.getX()) ** 2) +
                      ((second.getY() - first.getY()) ** 2))
        t = (CIR_RADIUS - .1) / d
        point = Point((((1 - t) * (first.getX())) + (t * second.getX())),
                      (((1 - t) * (first.getY())) + (t * second.getY())))
        return point