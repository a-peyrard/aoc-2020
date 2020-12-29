"""
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the
in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to
 you.
Their handheld game console won't turn on! They ask if you can take a look.
You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should
be able to fix it, but first you need to be able to run the code in isolation.
The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an
operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
    acc increases or decreases a single global value called the accumulator by the value given in the argument.
    For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction,
    the instruction immediately below it is executed next.
    jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument
    as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue
    to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
    nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
For example, consider the following program:
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:
nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then,5 the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next
instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes,
setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to
continue back at the first acc +1.
This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to
run any instruction a second time, you know it will never terminate.
Immediately before the program would run an instruction a second time, the value in the accumulator is 5.
Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the
 accumulator?

"""
import os
import re
from enum import Enum
from typing import List, NamedTuple, Iterable


class Type(Enum):
    NOP = 0
    ACC = 1
    JMP = 2


class Instruction(NamedTuple):
    type: Type
    value: int


INSTRUCTION_REGEX = re.compile(r"^(\w+) ([+-]\d+)$")


def play_instructions(instructions: List[Instruction]) -> int:
    executed_instructions = set()
    cursor = 0
    accumulator = 0
    while cursor not in executed_instructions:
        executed_instructions.add(cursor)
        instruction_type, value = instructions[cursor]
        if instruction_type == Type.ACC:
            accumulator += value
            cursor += 1
        elif instruction_type == Type.JMP:
            cursor += value
        elif instruction_type == Type.NOP:
            cursor += 1

    return accumulator


def _parse(raw_instructions: Iterable[str]) -> List[Instruction]:
    return list(
        map(
            lambda raw_instruction: _parse_instruction(raw_instruction.rstrip()),
            raw_instructions
        )
    )


def _parse_instruction(raw_instruction: str) -> Instruction:
    matcher = INSTRUCTION_REGEX.search(raw_instruction)
    if not matcher or len(matcher.groups()) != 2:
        raise ValueError(f"Unable to parse instruction {raw_instruction}")

    return Instruction(
        type=Type[matcher.group(1).upper()],
        value=int(matcher.group(2))
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        raw_instructions_from_file = list(file.readlines())

        solution_part1 = play_instructions(_parse(raw_instructions_from_file))
        print(f"solution (part1): {solution_part1}")
