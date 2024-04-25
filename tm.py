from typing import List, Union


class _Blank:
    def __str__(self):
        return '_'


subscript_numbers = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉"
}

yields_symbol = '⊢ₘ'


class StateTransitionFunction:
    def __init__(self,
                 read_character,
                 write_character,
                 move_direction: Union['Left', 'Right'],
                 new_state: Union['State', 'AcceptState', 'RejectState'],
                ):
        self.write_character = write_character
        self.read_character = read_character
        self.move_direction = move_direction
        self.new_state = new_state

class State:
    def __init__(self, name: str):
        new_name = []
        for char in name:
            if char in subscript_numbers:
                new_name.append(subscript_numbers[char])
            else:
                new_name.append(char)

        self.name = ''.join(new_name)

    def set_transition_functions(self, transition_functions: List[StateTransitionFunction]):
        self.transition_functions = {t.read_character: t for t in transition_functions}

    def get_transition_function(self, character) -> StateTransitionFunction:
        return self.transition_functions[character]


Blank = _Blank()
Left = object()
Right = object()
AcceptState = State('qₐ')
RejectState = State('qᵣ')


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

    def _print_trace(self, yields):
        first_half_temp = self.tape[:self.position]
        first_half = []
        for character in first_half_temp:
            if character is Blank and len(first_half) == 0:
                continue

            first_half.append(str(character))

        second_half_temp = reversed(self.tape[self.position:])
        second_half = []
        for character in second_half_temp:
            if character is Blank and len(second_half) == 0:
                continue

            second_half.append(str(character))
        second_half.reverse()

        if len(second_half) == 0:
            second_half = [str(Blank)]

        print(f'{yields_symbol if yields else ""}{" ".join(first_half)}{self.state.name}{" ".join(second_half)}')

    def execute(self, trace=True) -> bool:
        first = True
        while True:
            self._print_trace(not first)
            first = False

            transition_function = self.state.get_transition_function(self._read())
            self._process_transition_function(transition_function)
            self.state = transition_function.new_state
            if self.state is AcceptState:
                self._print_trace(first)
                return True
            elif self.state is RejectState:
                self._print_trace(first)
                return False


    def reset(self):
        self.tape = [Blank]
        self.state = self.initial_state
        self.position = 0