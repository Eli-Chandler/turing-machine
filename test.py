from tm import *


q_even = State('q0')
q_odd = State('q1')

q_even.set_transition_functions(
    [
        StateTransitionFunction(1, Blank, Right, q_odd),
        StateTransitionFunction(0, Blank, Right, q_even),
        StateTransitionFunction(Blank, Blank, Right, AcceptState)
    ]
)


q_odd.set_transition_functions(
    [
        StateTransitionFunction(1, Blank, Right, q_even),
        StateTransitionFunction(0, Blank, Right, q_odd),
        StateTransitionFunction(Blank, Blank, Right, RejectState)
    ]
)

m = TuringMachine(q_even)   # A turing machine that recognises if the tape contains an even number of 1's

m.set_tape([1, 1, 0, 1, 0, 1, 1])  # 5 1's
assert m.execute() is False

m.reset()

m.set_tape([1, 1, 1, 1, 0])  # 4 1's
assert m.execute() is True
