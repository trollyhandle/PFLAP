
# PFLAP
# Python Finite Automata Program
# Tyler Holland, Gaybi Igno

# Allows creation, conversion, and manipulation of DFAs and NFAs
# Operations allowed:
#   Create, edit NFA/DFA
#   Simulate inputs
#   Convert NFA to DFA
#   On two N/DFA inputs: union, intersect, difference, test equivalence

from classState import *
from graphics import *

WIN_HEIGHT = 600
WIN_WIDTH = 800
CIR_RADIUS = 20

toolbar_height = WIN_HEIGHT // 12

active_tool = 0
tool_boxes = []
tool_titles = ['Cursor', 'Add State', 'Add Transition', 'Move', 'Remove']

states = []
selected_state = None

# Store transitions at some point possibly in a dictionary
# { (symbol, a, b) : [instate, outstate] }
transitions = []

transition_begin_state = None
move_begin_state = None


def init_window(win):
    toolbar_box_width = WIN_WIDTH // len(tool_titles)

    padding = 10
    border = Line(Point(0, toolbar_height), Point(WIN_WIDTH, toolbar_height))
    border.setWidth(3)
    border.draw(win)

    def gen_callback(idx):  # create closure!
        return lambda: switchActiveButton(idx)

    for i in range(len(tool_titles)):
        rect = Rectangle(Point(i*toolbar_box_width+padding, padding),
                         Point((i+1)*toolbar_box_width-padding, toolbar_height-padding))
        rect.draw(win)
        tool_boxes.append(rect)

        b_test = tk.Button(win, text=tool_titles[i], command=gen_callback(i))
        win.create_window(rect.getCenter().x, rect.getCenter().y, window=b_test)

    tool_boxes[0].setOutline('blue')
    tool_boxes[0].setWidth(2)


def configRightClicks(win):
    initial = tk.BooleanVar()
    initial.set(False)
    win.rightMenu.add_command(label='Count Nodes', command=lambda: print('node count:', len(states)))
    win.rightMenu.add_checkbutton(label='check_test', variable=initial, command=lambda: print('check', initial.get()))


def switchActiveButton(next):
    global active_tool
    tool_boxes[active_tool].setOutline('black')
    tool_boxes[active_tool].setWidth(1)
    tool_boxes[next].setOutline('blue')
    tool_boxes[next].setWidth(2)
    active_tool = next
    return next


def main():
    print('yay pflap')

    win = GraphWin('PFLAP', WIN_WIDTH, WIN_HEIGHT, autoflush=False)
    init_window(win)

    configRightClicks(win)

    while True:
        try:
            clk_pt = win.getMouse()
        except GraphicsError:  # basically, closed window
            win.close()
            break  # aka return aka END OF THE LINE

        if clk_pt.getY() > toolbar_height:
            processClick(win, clk_pt, active_tool)


def find_containing_state(clk):
    # run backwards to preserve expected ordering (top-to-bottom)
    for q in reversed(states):
        if q.circle.contains(clk):
            return q
    return None


def processClick(win, clk, tool):
    if tool == 0:  # cursor (edit state/transition)
        global selected_state  # prevent local namespace shadowing
        q = find_containing_state(clk)
        if q is not None:
            if selected_state is not None and selected_state is not q:  # so it doesn't switch b, y, b
                selected_state.circle.setFill('yellow')
            selected_state = q
            q.circle.setFill('light blue')
        elif selected_state is not None:  # clicked in voidspace
            selected_state.circle.setFill('yellow')
            selected_state = None

    elif tool == 1:  # add state
        cir = Circle(clk, CIR_RADIUS)
        cir.setFill('yellow')
        cir.draw(win)
        new_state = State(clk, [], cir, "q" + str(len(states) + 1))
        new_state.label.draw(win)
        states.append(new_state)

    elif tool == 2:  # add transition
        global transition_begin_state  # prevent local namespace shadowing

        q = find_containing_state(clk)
        if q is not None:
            if transition_begin_state is None:  # first state
                q.circle.setFill('blue')
                transition_begin_state = q
            else:  # second state
                # Draw the transition
                line_first = movePoints(transition_begin_state.center, q.center)
                line_second = movePoints(q.center, transition_begin_state.center)
                ln = Line(line_first, line_second)
                ln.setArrow("last")
                ln.draw(win)

                #TODO: Temp way to store/print input symbols -- Put lambda if none
                    inSymbols = input("Input transition symbol(s): ")
                    symbols = inSymbols.split()

                    # Make Transition object
                trans = Transition(transition_begin_state, q, symbols, ln)
                    trans.drawSymbols(win)
                transitions.append(trans)

                # Add transition to each state -- used to app ln
                transition_begin_state.add_transition(trans)
                q.add_transition(trans)
                transition_begin_state.circle.setFill('yellow')
                transition_begin_state = None

        elif transition_begin_state is not None:  # clicked in voidspace
            transition_begin_state.circle.setFill('yellow')
            transition_begin_state = None

    elif tool == 3:  # move state
        global move_begin_state  # prevent local namespace shadowing
        if move_begin_state is not None:  # relocate
            ins = []
            outs = []
            ti = []
            to = []
            for i in range(len(move_begin_state.transitions)):
                for q in reversed(states):  # Temp remove transition from all states
                    if move_begin_state != q:
                        if move_begin_state.transitions[i] in q.transitions:
                            if (move_begin_state.transitions[i].inState == q):
                                ti.append(move_begin_state.transitions[i].symbols)
                                ins.append(q)
                            else:
                                to.append(move_begin_state.transitions[i].symbols)
                                outs.append(q)
                            q.transitions.remove(move_begin_state.transitions[i])
                transitions.remove(move_begin_state.transitions[i])

            # Redraw and update state
            move_begin_state.erase()
            move_begin_state.circle = Circle(clk, CIR_RADIUS)
            move_begin_state.center = clk
            move_begin_state.label = Text(clk, move_begin_state.name)
            move_begin_state.circle.setFill("yellow")
            move_begin_state.circle.draw(win)
            move_begin_state.label.draw(win)

            for i in range(len(ins)):   # Update where move_begin_state is the outState
                line_first = movePoints(move_begin_state.center, ins[i].center)
                line_second = movePoints(ins[i].center, move_begin_state.center)
                ln = Line(line_first, line_second)
                ln.setArrow("last")
                trans = Transition(move_begin_state, ins[i], ti[i], ln)    # Find way to keep symbols
                trans.drawSymbols(win)
                move_begin_state.add_transition(trans)
                ins[i].add_transition(trans)
                transitions.append(trans)

            for i in range(len(outs)):  # Update where move_begin_state is the inState
                line_first = movePoints(outs[i].center, move_begin_state.center)
                line_second = movePoints(move_begin_state.center, outs[i].center)
                ln = Line(line_first, line_second)
                ln.setArrow("last")
                trans = Transition(outs[i], move_begin_state, to[i], ln)   # Find way to keep symbols
                trans.drawSymbols(win)
                move_begin_state.add_transition(trans)
                outs[i].add_transition(trans)
                transitions.append(trans)

            # Redraw all transitions in and out of state
            move_begin_state.drawAll(win)
            move_begin_state = None
            return
        q = find_containing_state(clk)
        if q is not None:
            q.circle.setFill('light blue')
            move_begin_state = q

    elif tool == 4:  # remove state or transition
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            for i in range(len(q.transitions)):
                if q.tcontains(i, clk):
                    q.transitions[i].undraw()
                    del q.transitions[i]
            if q.circle.contains(clk):
                q.label.undraw()
                states.remove(q)
                q.erase()
                break

    else:  # undo, redo? other stuff
        print('tool not ready')
    win.flush()  # force update after any visual changes


def movePoints(first, second):
    """
    Takes two points and returns a point that is distance t from first point
    """
    d = math.sqrt(((second.getX() - first.getX()) ** 2) +
                  ((second.getY() - first.getY()) ** 2))
    t = (CIR_RADIUS - .1)/d
    point = Point((((1 - t) * (first.getX())) + (t * second.getX())),
                  (((1 - t) * (first.getY())) + (t * second.getY())))
    return point


main()
