"""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to
 take evasive actions!
Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety,
 it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you
 quickly volunteer.
The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer
input values. After staring at them for a few minutes, you work out what they probably mean:
    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship
is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the
following action were F.)
For example:
F10
N3
F7
R90
F11
These instructions would be handled as follows:
    F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
    N3 would move the ship 3 units north to east 10, north 3.
    F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
    R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
    F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position
and its north/south position) from its starting position is 17 + 8 = 25.
Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's
starting position?
"""
import os
from enum import Enum
from typing import NamedTuple, List, Iterable, Tuple


class Position(NamedTuple):
    x: int = 0
    y: int = 0


class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


class Type(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


class Instruction(NamedTuple):
    type: Type
    value: int


def move(instructions: List[Instruction],
         position: Position,
         direction: Direction) -> Position:

    for instruction in instructions:
        position, direction = _move_instruction(instruction, position, direction)

    return position


def _move_instruction(instruction: Instruction,
                      position: Position,
                      direction: Direction) -> Tuple[Position, Direction]:

    if instruction.type == Type.EAST:
        position = Position(position.x + instruction.value, position.y)
    elif instruction.type == Type.WEST:
        position = Position(position.x - instruction.value, position.y)
    elif instruction.type == Type.NORTH:
        position = Position(position.x, position.y + instruction.value)
    elif instruction.type == Type.SOUTH:
        position = Position(position.x, position.y - instruction.value)
    elif instruction.type == Type.FORWARD:
        # simulate an instruction with a direction being the current direction
        position, direction = _move_instruction(
            Instruction(Type[direction.name], instruction.value),
            position,
            direction
        )
    elif instruction.type == Type.LEFT:
        direction = _turn(-1 * instruction.value, direction)
    elif instruction.type == Type.RIGHT:
        direction = _turn(instruction.value, direction)

    return position, direction


def _turn(value: int, direction: Direction) -> Direction:
    new_value = (direction.value + value) % 360
    return Direction(new_value)


def calculate_manhattan_distance(orig: Position, dest: Position) -> int:
    return abs(dest.x - orig.x) + abs(dest.y - orig.y)


def _parse(lines: Iterable[str]) -> List[Instruction]:
    return [_parse_instruction(line) for line in lines]


def _parse_instruction(line: str) -> Instruction:
    safe_line = line.rstrip()
    raw_type = safe_line[0]
    value = int(safe_line[1:])

    return Instruction(
        type=Type(raw_type),
        value=value
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        instructions_from_file = _parse(file.readlines())

        initial_position = Position()
        solution_part1 = calculate_manhattan_distance(
            orig=initial_position,
            dest=move(
                instructions=instructions_from_file,
                position=initial_position,
                direction=Direction.EAST
            )
        )
        print(f"solution (part1): {solution_part1}")
        assert solution_part1 == 1007
