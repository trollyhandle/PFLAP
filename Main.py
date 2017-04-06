
# PFLAP
# Python Finite Automata Program
# Tyler Holland, Gaybi Igno

# Allows creation, conversion, and manipulation of DFAs and NFAs
# Operations allowed:
#   Create, edit NFA/DFA
#   Simulate inputs
#   Convert NFA to DFA
#   On two N/DFA inputs: union, intersect, difference, test equivalence

from classState import State
from graphics import *

WIN_HEIGHT = 600
WIN_WIDTH = 800

toolbar_height = WIN_HEIGHT // 10

tool_boxes = []
tool_titles = ['Cursor', 'Add State', 'Add Transition', 'Move', 'Remove']

states = []
selected_state = None

# Store transitions at some point possibly in a dictionary
transition_table = dict()

transition_begin_state = None
move_begin_state = None


def init_window(win):
    toolbar_box_width = WIN_WIDTH // len(tool_titles)

    padding = 10
    border = Line(Point(0, toolbar_height), Point(WIN_WIDTH, toolbar_height))
    border.setWidth(3)
    border.draw(win)

    for i in range(len(tool_titles)):
        rect = Rectangle(Point(i*toolbar_box_width+padding, padding),
                         Point((i+1)*toolbar_box_width-padding, toolbar_height-padding))
        rect.draw(win)
        txt = Text(rect.getCenter(), tool_titles[i])
        txt.draw(win)
        tool_boxes.append(rect)
    tool_boxes[0].setOutline('blue')
    tool_boxes[0].setWidth(2)

def main():
    print('yay pflap')

    win = GraphWin('PFLAP', WIN_WIDTH, WIN_HEIGHT)
    init_window(win)

    active_tool = 0
    while True:
        try:
            clk_pt = win.getMouse()
        except GraphicsError:  # basically, closed window
            win.close()
            break  # aka return aka end of the line

        if clk_pt.getY() < toolbar_height:
            for i, box in enumerate(tool_boxes):
                if box.contains(clk_pt):
                    tool_boxes[active_tool].setOutline('black')
                    tool_boxes[active_tool].setWidth(1)
                    box.setOutline('blue')
                    box.setWidth(2)
                    active_tool = i
        else:
            processClick(win, clk_pt, active_tool)


def processClick(win, clk, tool):
    if tool == 0:  # cursor (edit state/transition)
        did_select = False
        global selected_state  # prevent local namespace shadowing
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.circle.contains(clk):
                if selected_state is not None:
                    selected_state.setFill('yellow')
                selected_state = q
                q.setFill('light blue')
                did_select = True
                break
        if not did_select and selected_state is not None:  # clicked in voidspace
            selected_state.setFill('yellow')
            selected_state = None

    elif tool == 1:  # add state
        cir = Circle(clk, 20)
        cir.setFill('yellow')
        cir.draw(win)
        new_state = State(clk, [], cir, "q" + str(len(states) + 1))
        new_state.label.draw(win)
        states.append(new_state)

    elif tool == 2:  # add transition
        did_select = False
        global transition_begin_state  # prevent local namespace shadowing
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.circle.contains(clk):
                if transition_begin_state is None:  # first state
                    q.circle.setFill('blue')
                    transition_begin_state = q
                else:  # second state
                    ln = Line(transition_begin_state.center, q.center)
                    ln.setArrow("last")
                    ln.draw(win)

                    transition_begin_state.add_transition(ln)
                    q.add_transition(ln)
                    transition_begin_state.circle.setFill('yellow')
                    transition_begin_state = None
                did_select = True
                break
        if not did_select and transition_begin_state is not None:  # clicked in voidspace
            transition_begin_state.circle.setFill('yellow')
            transition_begin_state = None

    elif tool == 3:  # move state
        global move_begin_state  # prevent local namespace shadowing
        if move_begin_state is not None:  # relocate

            for i in range(len(move_begin_state.transitions)):
                first, second = move_begin_state.transitions[i].getP1(), move_begin_state.transitions[i].getP2()
                if (move_begin_state.circle.contains(first)):
                    first = clk
                if (move_begin_state.circle.contains(second)):
                    second = clk

                toFix = []
                for q in reversed(states):
                    if move_begin_state != q:
                        if move_begin_state.transitions[i] in q.transitions:
                            q.transitions.remove(move_begin_state.transitions[i])
                            toFix.append(q)

                move_begin_state.transitions[i].undraw()
                move_begin_state.transitions[i] = Line(first, second)
                move_begin_state.transitions[i].setArrow("last")
                for j in range(len(toFix)):
                    toFix[j].add_transition(move_begin_state.transitions[i])

                move_begin_state.transitions[i].undraw()
            move_begin_state.circle.undraw()
            move_begin_state.label.undraw()
            move_begin_state.circle = Circle(clk, 20)
            move_begin_state.center = clk
            move_begin_state.label = Text(clk, move_begin_state.name)
            move_begin_state.circle.setFill("yellow")
            move_begin_state.circle.draw(win)
            move_begin_state.label.draw(win)
            move_begin_state.drawAll(win)
            move_begin_state = None
            return
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.contain(clk):
                q.circle.setFill('light blue')
                move_begin_state = q
                break

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


main()
