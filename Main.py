
# PFLAP
# Python Finite Automata Program
# Tyler Holland, Gaybi Igno

# Allows creation, conversion, and manipulation of DFAs and NFAs
# Operations allowed:
#   Create, edit NFA/DFA
#   Simulate inputs
#   Convert NFA to DFA
#   On two N/DFA inputs: union, intersect, difference, test equivalence

from DFA import *

WIN_HEIGHT = 600
WIN_WIDTH = 800
CIR_RADIUS = 20

toolbar_height = 50

active_tool = 0
#: :type: list of Rectangle
tool_boxes = []  # type hinting is neat!
#: :type: list of State
states = []

selected_state = None
transition_begin_state = None
move_begin_state = None


def init_window(win):
    """ 
    :param win: graphics window to initialize 
    @type win tk.Canvas """
    tool_titles = ['Cursor', 'Add State', 'Add Transition', 'Move', 'Remove', 'Simulate']
    toolbar_box_width = WIN_WIDTH // len(tool_titles)

    padding = 10
    border = Line(Point(0, toolbar_height), Point(WIN_WIDTH, toolbar_height))
    border.setWidth(3)
    border.draw(win)

    def gen_callback(idx):  # create closure!
        return lambda: switchActiveButton(idx, win)

    for i in range(len(tool_titles)):
        rect = Rectangle(Point(i*toolbar_box_width+padding, padding),
                         Point((i+1)*toolbar_box_width-padding, toolbar_height-padding))
        rect.draw(win)
        tool_boxes.append(rect)

        button_width = 12
        button = tk.Button(win, text=tool_titles[i], width=button_width, command=gen_callback(i))

        win.create_window(rect.getCenter().x, rect.getCenter().y, window=button)

    tool_boxes[0].setOutline('blue')
    tool_boxes[0].setWidth(2)


def configRightClicks(win):
    initial = tk.BooleanVar()
    initial.set(False)
    win.rightMenu.add_command(label='Count Nodes', command=lambda: print('node count:', len(states)))
    # win.rightMenu.add_checkbutton(label='check_test', variable=initial, command=lambda: print('check', initial.get()))


def switchActiveButton(next_tool, win):
    global active_tool
    tool_boxes[active_tool].setOutline('black')
    tool_boxes[active_tool].setWidth(1)
    tool_boxes[next_tool].setOutline('blue')
    tool_boxes[next_tool].setWidth(2)
    active_tool = next_tool
    if active_tool == 4:
        win.config(cursor="X_cursor")
    else:
        win.config(cursor="left_ptr")


def main():
    print('yay pflap')
    from_scratch = False

    win = GraphWin('PFLAP', WIN_WIDTH, WIN_HEIGHT, autoflush=False)
    init_window(win)

    configRightClicks(win)

    if from_scratch:  # create brand-new dfa
        dfa = DFA()
    else:  # generate dfa
        dfa = DFA.example()
        global states
        states = dfa.inflate(win, toolbar_height)

    while True:
        try:
            clk_pt = win.getMouse()
        except GraphicsError:  # basically, closed window
            win.close()
            break  # aka return aka END OF THE LINE

        if clk_pt.getY() > toolbar_height:
            processClick(win, clk_pt, active_tool, dfa)
        dfa.print()
        print()


def find_containing_state(clk):
    # run backwards to preserve expected ordering (top-to-bottom)
    for q in reversed(states):
        if q.circle.contains(clk):
            return q
    return None


def processClick(win, clk, tool, dfa):
    if tool == 0:  # cursor (edit state/transition)
        global selected_state  # prevent local namespace shadowing
        q = find_containing_state(clk)
        if q is not None:
            if selected_state is not None and selected_state is not q:  # so it doesn't switch b, y, b
                selected_state.circle.setFill(selected_state.color)
            selected_state = q
            q.circle.setFill('light blue')
        elif selected_state is not None:  # clicked in voidspace
            selected_state.circle.setFill(selected_state.color)
            selected_state = None

    elif tool == 1:  # add state
        new_id = dfa.get_free_id()
        new_node = DFANode("q" + str(new_id), center=clk, id=new_id)
        dfa.add_node(new_node)
        new_state = State(new_node)
        new_state.draw(win)
        states.append(new_state)

    elif tool == 2:  # add transition
        global transition_begin_state  # prevent local namespace shadowing

        q = find_containing_state(clk)
        if q is not None:
            if transition_begin_state is None:  # first state
                q.circle.setFill('blue')
                transition_begin_state = q
            else:  # second state

                # TODO: Temp way to store/print input symbols -- Put lambda if none
                symbols = input("Input transition symbol(s): ").split()
                if len(symbols) == 0:
                    symbols = "λ"

                # Make and draw Transition object
                if not transition_begin_state.check_existing(q, symbols, win):  # If not duplicate
                    if not transition_begin_state.check_reverse(q, symbols, win):   # If no reverse transition
                        trans = Transition(transition_begin_state, q, symbols)
                        trans.draw(win)

                        # Add transition to each state -- used to app ln
                        transition_begin_state.add_transition(trans)
                        if not q.duplicate(q):
                            q.add_transition(trans)
                transition_begin_state.circle.setFill(transition_begin_state.color)
                transition_begin_state = None

        elif transition_begin_state is not None:  # clicked in voidspace
            transition_begin_state.circle.setFill(transition_begin_state.color)
            transition_begin_state = None

    elif tool == 3:  # move state
        global move_begin_state  # prevent local namespace shadowing
        if move_begin_state is not None:  # state ready to relocate
            # Redraw and update state and transitions
            move_begin_state.move(clk, win)
            #move_begin_state.circle.setFill("yellow")
            move_begin_state = None
            return
        q = find_containing_state(clk)
        if q is not None:
            q.circle.setFill('light blue')
            move_begin_state = q

    elif tool == 4:  # remove state or transition
        # win.config(cursor="X_cursor")  # todo fix when cursor is present
        for q in reversed(states):  # run backwards to preserve expected ordering (top-to-bottom)
            for i in range(len(q.transitions)):
                if q.tcontains(i, clk):
                    # todo remove transition from node
                    q.transitions[i].remove()
                    break
            if q.circle.contains(clk):
                dfa.remove_node(q.node)
                states.remove(q)
                q.delete()
                break

    # elif tool == 5:  # simulate input

    else:  # undo, redo? other stuff
        print('tool not ready gtfo')  # new kmessage more accurately reflects my mental state

    win.flush()  # force update after any visual changes

main()
