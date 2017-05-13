# State class
# Tyler Holland, Gaybi Igno
# Maintains data on a single state in a N/DFA, and its associated transitions

from graphics import *
from math import *
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
        self.transitions = []

    def equal(self, other):
        if self.node == other.node and self.circle == other.circle \
                and self.label == other.label and self.color == other.color:
            if len(self.transitions) == len(other.transitions):
                for trans in self.transitions:
                    if trans not in other.transitions:
                        return False
                return True
        return False

    # Draws state with given color and border width
    def draw(self, win):
        self.circle.setWidth(1)
        self.color = 'yellow'
        if self.node.is_final:
            self.circle.setWidth(3)
        if self.node.is_initial:
            self.color = 'plum'
        self.circle.setFill(self.color)
        self.circle.draw(win)
        self.label.draw(win)

    # Draw state and transition(s)
    def drawAll(self, win):
        self.draw(win)
        # Update transitions
        for line in self.transitions:
            line.draw(win)

    # Print information about the state
    def print(self):
        print("center: ", self.node.center)
        print("circle: ", self.circle)
        print("circle: ", self.color)
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
        if self.transitions[index].inState.equal(self.transitions[index].outState):
            return self.point_in_triangle(click, self.transitions[index].line.getPoints())
        first, second = self.transitions[index].line.getP1(), self.transitions[index].line.getP2()
        return first.distanceTo(click) + second.distanceTo(click) == first.distanceTo(second)

    # Returns if point is in self-transition triangle
    def point_in_triangle(self, click, list_of_points):
        first_check = self.tri_test(click, list_of_points[0], list_of_points[1]) < 0.0
        second_check = self.tri_test(click, list_of_points[1], list_of_points[2]) < 0.0
        third_check = self.tri_test(click, list_of_points[2], list_of_points[0]) < 0.0
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
            if t.inState == inState and t.outState == self:
                trans = t
        if trans is None:
            return False
        trans.add_symbol(symbols, win)
        return True

    # If reverse transition exists, redraw transitions
    def check_reverse(self, inState, symbols, win):
        trans_out = None
        # Find the reverse transition
        for t in inState.transitions:
            if t.inState == self and t.outState == inState:
                trans_out = t
        if trans_out is None:
            return False

        # Find new points to draw transition line
        if self.find_degree(inState):
            top_in = self.find_edge(Point(self.getCenter().getX() - 5, self.getCenter().getY()),
                                    Point(inState.getCenter().getX() - 5, inState.getCenter().getY()))
            top_out = inState.find_edge(Point(inState.getCenter().getX() - 5, inState.getCenter().getY()),
                                        Point(self.getCenter().getX() - 5, self.getCenter().getY()))

            bottom_out = self.find_edge(Point(self.getCenter().getX() + 5, self.getCenter().getY()),
                                        Point(inState.getCenter().getX() + 5, inState.getCenter().getY()))
            bottom_in = inState.find_edge(Point(inState.getCenter().getX() + 5, inState.getCenter().getY()),
                                          Point(self.getCenter().getX() + 5, self.getCenter().getY()))
        else:
            top_in = self.find_edge(Point(self.getCenter().getX(), self.getCenter().getY() - 5),
                                        Point(inState.getCenter().getX(), inState.getCenter().getY() - 5))
            top_out = inState.find_edge(Point(inState.getCenter().getX(), inState.getCenter().getY() - 5),
                                    Point(self.getCenter().getX(), self.getCenter().getY() - 5))

            bottom_out = self.find_edge(Point(self.getCenter().getX(), self.getCenter().getY() + 5),
                                          Point(inState.getCenter().getX(), inState.getCenter().getY() + 5))
            bottom_in = inState.find_edge(Point(inState.getCenter().getX(), inState.getCenter().getY() + 5),
                                    Point(self.getCenter().getX(), self.getCenter().getY() + 5))

        # Redraw trans going out
        trans_out.undraw()
        trans_out.line = Line(top_in, top_out)
        trans_out.line.setArrow("last")
        trans_out.line.draw(win)
        s = ", ".join(trans_out.symbols)
        point = Point(trans_out.line.getCenter().getX(), trans_out.line.getCenter().getY() - 10)
        trans_out.text = Text(point, s)
        trans_out.text.draw(win)

        # Draw transition going in
        trans_in = None
        new = False
        for t in self.transitions:
            if t.inState == inState:
                trans_in = t
                trans_in.undraw()
        if trans_in is None:
            trans_in = Transition(self, inState, symbols)
            new = True

        trans_in.line = Line(bottom_in, bottom_out)
        trans_in.line.setArrow("last")
        trans_in.line.draw(win)
        s = ", ".join(trans_in.symbols)
        point = Point(trans_in.line.getCenter().getX(), trans_in.line.getCenter().getY() + 10)
        trans_in.text = Text(point, s)
        trans_in.text.draw(win)
        trans_in.above = False
        if new:
            self.add_transition(trans_in)
            inState.add_transition(trans_in)
        return True

    # Find the edge of the state in relation to another
    def find_edge(self, other, this):
        dx = other.getX() - this.getX()
        dy = other.getY() - this.getY()
        rads = atan2(dy, dx)
        rads %= (2 * pi)
        X = this.getX() + (CIR_RADIUS * math.cos(rads))
        Y = this.getY() + (CIR_RADIUS * math.sin(rads))
        return Point(X, Y)

    # Returns if transition has more vertical or horizontal alignment
    def find_degree(self, other):
        dx = other.circle.getCenter().getX() - self.circle.getCenter().getX()
        dy = other.circle.getCenter().getY() - self.circle.getCenter().getY()
        rads = atan2(dy, dx)
        rads %= (2 * pi)
        deg = degrees(rads)
        print("deg:", deg)
        if 120 > deg > 60 or 240 < deg < 300:
            return True
        return False

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

        # Set color back from light blue
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
    # text - Text object representation of symbols
    # line - Transition line (Line or Polygon)
    # arrow - Polygon (triangle) object on self-transitions
    # above - Differentiate when text is drawn above or below line

    def __init__(self, outState, inState, symbols):
        #: :type: State
        self.inState = inState
        #: :type: State
        self.outState = outState
        self.symbols = []
        for i in symbols:
            self.symbols.append(i)
        self.text = None
        self.line = None
        self.arrow = None
        self.above = True

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

        # Draw symbol(s) above the transition
        if self.outState == self.inState:
            all_points = self.line.getPoints()
            point = Point(all_points[0].getX(), all_points[0].getY() - CIR_RADIUS - 5)
        else:
            if self.above:
                point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
            else:
                point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() + 10)
        self.text = Text(point, s)
        self.text.draw(win)

    # Draw
    def draw(self, win):
        if self.line is not None: # This only identifies during move, not create
            self.line.undraw()
            self.text.undraw()
            if self.arrow is not None:
                self.arrow.undraw()
        if self.inState == self.outState: # Check if self-transition
            self.self_transition(win)
        else:
            if not self.outState.check_reverse(self.inState, self.symbols, win):
                line_first = self.movePoints(self.firstCenter(), self.secondCenter())
                line_second = self.movePoints(self.secondCenter(), self.firstCenter())
                self.line = Line(line_first, line_second)
                self.line.setArrow("last")
                self.line.draw(win)

                s = ", ".join(self.symbols)
                if self.above:
                    point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() - 10)
                else:
                    point = Point(self.line.getCenter().getX(), self.line.getCenter().getY() + 10)
                self.text = Text(point, s)
                self.text.draw(win)

    # Erase transition from the window
    def undraw(self):
        self.line.undraw()
        self.text.undraw()
        if self.arrow is not None:
            self.arrow.undraw()

    # Deletes transition completely
    def remove(self):
        self.undraw()
        self.outState.remove_transition(self)
        self.inState.remove_transition(self)

    # Takes two points and returns a point that is distance t from first point
    def movePoints(self, first, second):
        if first.x == second.x and first.y == second.y:
            return first
        d = math.sqrt(((second.getX() - first.getX()) ** 2) +
                      ((second.getY() - first.getY()) ** 2))
        t = (CIR_RADIUS - .1) / d
        point = Point((((1 - t) * (first.getX())) + (t * second.getX())),
                      (((1 - t) * (first.getY())) + (t * second.getY())))
        return point

    # Draws the self transition
    def self_transition(self, win):
        top = Point(self.inState.node.center.getX(), self.inState.node.center.getY() - CIR_RADIUS)
        left = Point(top.getX() - CIR_RADIUS, top.getY() - CIR_RADIUS)
        right = Point(left.getX() + (2 * CIR_RADIUS), left.getY())
        self.line = Polygon(top, left, right)
        self.line.draw(win)

        l_left = Point(top.getX() + (CIR_RADIUS / 4), top.getY() - (CIR_RADIUS / 2.2))
        l_right = Point(top.getX() + (CIR_RADIUS / 2.2), top.getY() - (CIR_RADIUS / 4))
        self.arrow = Polygon(top, l_left, l_right)
        self.arrow.setFill("black")
        self.arrow.draw(win)

        s = ", ".join(self.symbols)
        point = Point(top.getX(), top.getY() - CIR_RADIUS - 5)
        self.text = Text(point, s)
        self.text.draw(win)