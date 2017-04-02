
# PFLAP
# Python Finite Automata Program
# Tyler Holland, Gaybi Igno

# Allows creation, conversion, and manipulation of DFAs and NFAs
# Operations allowed:
#   Create, edit NFA/DFA
#   Simulate inputs
#   Convert NFA to DFA
#   On two N/DFA inputs: union, intersect, difference, test equivalence

from graphics import *

WIN_HEIGHT = 600
WIN_WIDTH = 800

toolbar_height = WIN_HEIGHT // 10

tool_boxes = []
tool_titles = ['Cursor', 'Add State', 'Add Transition', 'Move', 'Remove']

states = []
selected_state = None

transition_begin_state = None
move_begin_state = None


def init_window(win):
    toolbar_box_width = WIN_WIDTH // len(tool_titles)

    border = Line(Point(0, toolbar_height), Point(WIN_WIDTH, toolbar_height))
    border.setWidth(3)
    border.draw(win)
    padding = 10

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
            if q.contains(clk):
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
        states.append(cir)

    elif tool == 2:  # add transition
        did_select = False
        global transition_begin_state  # prevent local namespace shadowing
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.contains(clk):
                if transition_begin_state is None:  # first state
                    q.setFill('blue')
                    transition_begin_state = q
                else:  # second state
                    ln = Line(transition_begin_state.getCenter(), q.getCenter())
                    ln.draw(win)
                    transition_begin_state.setFill('yellow')
                    transition_begin_state = None
                did_select = True
                break
        if not did_select and transition_begin_state is not None:  # clicked in voidspace
            transition_begin_state.setFill('yellow')
            transition_begin_state = None

    elif tool == 3:  # move state
        global move_begin_state  # prevent local namespace shadowing
        if move_begin_state is not None:  # relocate
            dx = clk.getX() - move_begin_state.getCenter().getX()
            dy = clk.getY() - move_begin_state.getCenter().getY()
            move_begin_state.move(dx, dy)
            move_begin_state.setFill('yellow')
            move_begin_state = None
            return
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.contains(clk):
                q.setFill('light blue')
                move_begin_state = q
                break

    elif tool == 4:  # remove state
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            if q.contains(clk):
                states.remove(q)
                q.undraw()
                break

    else:  # undo, redo? other stuff
        print('tool not ready')


main()
