# PFLAP
Python tool for creating NFA/DFA and performing certain operations

By: Tyler Holland and Gaybi Igno

Problem to solve:
Create a tool similar to JFLAP (http://www.jflap.org/) that allows a user to create a DFA or an NFA and perform the
following operations:

        a) simulate on a given input
        b) convert from NFA to DFA,
        c) take as input two DFA’s (or NFA’s) and perform the following operations:
                (i) union
                (ii) intersection
                (iii) complement, etc.
        d) take as input two DFA’s and test if they are equivalent.

This tool will have an interface similar to JFLAP in several ways:

        The main window will be mostly space for creating and editing N/DFAs
        There will be a toolbox bar at the top

        Users can create states and transitions
        Users can set and edit labels on states/transitions
        Users can execute the supported operations via the aforementioned toolbox

        /***** optional extras *****/
        Graphs can be saved to file, and loaded from files (maybe '*.pff' ?)
        DFA's can be generated from a transition matrix input (csv-style?)
        
