# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions

from graphics import *
CIR_RADIUS = 20


class State:
    # vars:
    # node - DFANode this State is based on
    # circle - Circle object in the canvas
    # color - Color of state based on if initial or final
    # transitions [] - Transitions with this state as source or destination
    # label - Text object in the canvas

    def __init__(self, node):
        self.node = node
        self.circle = Circle(node.center, CIR_RADIUS)
        self.label = Text(node.center, node.name)
        self.color = ""
        #: :type: list of Transition
        self.transitions = []  # todo list or dict?

    # Draws state with given color
    def draw(self, win):
        if self.node.is_final:
            self.color = 'lightsalmon'
        elif self.node.is_initial:
            self.color = 'darkseagreen'
        else:
            self.color ='yellow'
        self.circle.setFill(self.color)
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

    # Add transition to state's transition list
    def add_transition(self, line):
        self.transitions.append(line)

    # Remove transition from state's transition list
    def remove_transition(self, line):
        if line in self.transitions:
            self.transitions.remove(line)

    # Returns center of state circle
    def getCenter(self):
        return self.node.getCenter()

    # If transition line was clicked
    def tcontains(self, index, click):
        print("idx:", index)
        if self.transitions[index].inState == self.transitions[index].outState:
            return self.point_in_triangle(click, self.transitions[index].line.getPoints())
        first, second = self.transitions[index].line.getP1(), self.transitions[index].line.getP2()
        return first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second)

    # Returns if point is in self-transition triangle
    def point_in_triangle(self, click, list_of_points):
        first_check = self.tri_test( click, list_of_points[0], list_of_points[1] ) < 0.0
        second_check = self.tri_test( click, list_of_points[1], list_of_points[2] ) < 0.0
        third_check = self.tri_test( click, list_of_points[2], list_of_points[0] ) < 0.0

        return first_check == second_check == third_check

    # Helper for point_in_triangle
    def tri_test(self, p1, p2, p3):
        return (p1.getX() - p3.getX()) * (p2.getY() - p3.getY()) - \
               (p2.getX() - p3.getX()) * (p1.getY() - p3.getY())

    # Checks if the transition exists
    def duplicate(self, inState):
        for t in self.transitions:
            if t.inState == inState:
                return True
        return False

    # If transition exists, add new symbols
    def check_existing(self, inState, symbols, win):
        trans = None
        for t in self.transitions:
            if t.inState == inState:
                trans = t
        if trans == None:
            return False
        trans.add_symbol(symbols, win)
        return True

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

        # Set color back from lightblue
        self.circle.setFill(self.color)

    # Delete state and all of its transitions
    def delete(self):
        self.circle.undraw()
        self.color = ""
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

    # Add symbol(s) on existing transition
    def add_symbol(self, symbol, win):
        self.text.undraw()
        if type(symbol) is list:
            for i in symbol:
                self.symbols.append(i)
        else:
            self.symbols.append(symbol)
        s = ", ".join(self.symbols)

        # Draw symbol(s) alove the transition
        if self.outState == self.inState:
            all_points = self.line.getPoints()
            point = Point(all_points[0].getX(), all_points[0].getY() - CIR_RADIUS - 5)
        else:
            point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
        self.text = Text(point, s)
        self.text.draw(win)

    # Draw
    def draw(self, win):
        if self.line is not None: # This only identifies during move, not create
            self.line.undraw()
            self.text.undraw()
        if self.inState == self.outState: # Check if self-transition
            self.self_transition(win)
        else:
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

    # Deletes transition
    def remove(self):
        self.undraw()
        self.outState.remove_transition(self)
        self.inState.remove_transition(self)

    def movePoints(self, first, second):
        """
        Takes two points and returns a point that is distance t from first point
        """
        if first.x == second.x and first.y == second.y:
            # todo self-transition??
            return first
        d = math.sqrt(((second.getX() - first.getX()) ** 2) +
                      ((second.getY() - first.getY()) ** 2))
        t = (CIR_RADIUS - .1) / d
        point = Point((((1 - t) * (first.getX())) + (t * second.getX())),
                      (((1 - t) * (first.getY())) + (t * second.getY())))
        return point

    def self_transition(self, win):
        """
        Draws the self transition
        """
        top = Point(self.inState.node.center.getX(), self.inState.node.center.getY() - CIR_RADIUS)
        left = Point(top.getX() - CIR_RADIUS, top.getY() - CIR_RADIUS)
        right = Point(left.getX() + (2 * CIR_RADIUS), left.getY())

        self.line = Polygon(top, left, right)
        self.line.setOutline("black")
        self.line.setFill("white")
        self.line.draw(win)

        s = ", ".join(self.symbols)
        point = Point(top.getX(), top.getY() - CIR_RADIUS - 5)
        self.text = Text(point, s)
        self.text.draw(win)