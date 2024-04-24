from typing import List, Union

Blank = object()
Left = object()
Right = object()
AcceptState = object()
RejectState = object()


class StateTransitionFunction:
    def __init__(self,
                 read_character,
                 write_character,
                 move_direction: Union[Left, Right],
                 new_state: Union['State', AcceptState, RejectState],
                ):
        self.write_character = write_character
        self.read_character = read_character
        self.move_direction = move_direction
        self.new_state = new_state


class State:
    def set_transition_functions(self, transition_functions: List[StateTransitionFunction]):
        self.transition_functions = {t.read_character: t for t in transition_functions}


    def get_transition_function(self, character) -> StateTransitionFunction:
        return self.transition_functions[character]


class TuringMachine:
    def __init__(self, initial_state: State):
        self.tape = [Blank]
        self.initial_state = initial_state
        self.state = initial_state
        self.position = 0

    def set_tape(self, tape: List):
        self.tape = tape

    def read_tape(self):
        return self.tape[:]  # Return a copy of the tape

    def _read(self):
        if self.position == len(self.tape):
            self.tape.append(Blank)

        return self.tape[self.position]

    def _write(self, character):
        if self.position == len(self.tape):
            self.tape.append(Blank)

        self.tape[self.position] = character

    def _move_left(self):
        if self.position == 0:
            return

        self.position -= 1

    def _move_right(self):
        self.position += 1
        if self.position == len(self.tape):
            self.tape.append(Blank)

    def _process_transition_function(self, transition_function: StateTransitionFunction):
        self._write(transition_function.write_character)

        if transition_function.move_direction == Left:
            self._move_left()
        else:
            self._move_right()

    def execute(self) -> bool:
        while True:
            transition_function = self.state.get_transition_function(self._read())
            self._process_transition_function(transition_function)
            if transition_function.new_state == AcceptState:
                return True
            elif transition_function.new_state == RejectState:
                return False
            else:
                self.state = transition_function.new_state

    def reset(self):
        self.tape = [Blank]
        self.state = self.initial_state
        self.position = 0