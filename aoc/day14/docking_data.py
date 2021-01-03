"""
--- Day 14: Docking Data ---
As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port
isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in
the docking program's memory.
After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its
initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!
The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and
memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11
 would write the value 11 to memory address 8.
The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the
left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values
immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves
 the bit in the value unchanged.
For example, consider the following program:
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every
written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.
The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the
 mask is applied as follows:
value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to
address 7:
value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the
program tries to write 0 to address 8:
value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there previously.
To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization
program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above
example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
Execute the initialization program. What is the sum of all values left in memory after it completes? (Do not truncate
the sum to 36 bits.)

--- Part Two ---
For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be
using version 2 of the decoder chip!
A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder.
Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the
destination memory address in the following way:
    If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating.
A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating
bits will take on all possible values, potentially causing many memory addresses to be written all at once!
For example, consider the following program:
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
When this program goes to write to memory address 42, it first applies the bitmask:
address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X
After applying the mask, four bits are overwritten, three of which are different, and two of which are floating.
Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are
written:
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)
Next, the program is about to write to memory address 26 with a different bitmask:
address: 000000000000000000000000000000011010  (decimal 26)
mask:    00000000000000000000000000000000X0XX
result:  00000000000000000000000000000001X0XX
This results in an address with three floating bits, causing writes to eight memory addresses:
000000000000000000000000000000010000  (decimal 16)
000000000000000000000000000000010001  (decimal 17)
000000000000000000000000000000010010  (decimal 18)
000000000000000000000000000000010011  (decimal 19)
000000000000000000000000000000011000  (decimal 24)
000000000000000000000000000000011001  (decimal 25)
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of
 all values left in memory at the end of the program. In this example, the sum is 208.
Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in
 memory after it completes?

"""
import os
import re
from typing import Dict, Iterable, Tuple, List

MASK_LINE_PREFIX = "mask = "
MEM_LINE_REGEX = re.compile(r"mem\[(\d+)] = (\d+)")


class Mask:
    _GLOBAL_MASK = (1 << 36) - 1  # we want to work on 36bits only

    @classmethod
    def noop(cls) -> 'Mask':
        return cls(0, Mask._GLOBAL_MASK)

    @classmethod
    def parse(cls,
              raw_mask: str) -> 'Mask':
        negative_mask = Mask._GLOBAL_MASK
        positive_mask = 0
        for idx, c in enumerate(raw_mask):
            if c == "X":
                continue
            bit_index = 35 - idx
            if c == "1":
                positive_mask |= 1 << bit_index
            else:
                negative_mask &= (Mask._GLOBAL_MASK ^ 1 << bit_index)

        return cls(positive_mask, negative_mask)

    def __init__(self, positive_mask: int, negative_mask: int):
        self._positive_mask = positive_mask
        self._negative_mask = negative_mask

    def apply(self, val: int) -> int:
        return (val & self._negative_mask) | self._positive_mask


def execute_program(lines: Iterable[str]) -> Dict[int, int]:
    mask = Mask.noop()
    memory = {}
    for line in lines:
        safe_line = line.rstrip()
        if safe_line.startswith(MASK_LINE_PREFIX):
            mask = Mask.parse(safe_line[len(MASK_LINE_PREFIX):])
        else:
            address, value = _extract_mem_instruction(safe_line)
            memory[address] = mask.apply(value)

    return memory


def _extract_mem_instruction(line: str) -> Tuple[int, int]:
    matcher = MEM_LINE_REGEX.search(line)
    if not matcher or len(matcher.groups()) != 2:
        raise ValueError(f"Unable to parse mem instruction {line}")

    return int(matcher.group(1)), int(matcher.group(2))


def sum_memory(memory: Dict[int, int]) -> int:
    return sum(memory.values())


class MaskV2:
    @classmethod
    def noop(cls) -> 'MaskV2':
        return cls(["0"] * 36)

    @classmethod
    def parse(cls,
              raw_mask: str) -> 'MaskV2':
        return cls(list(raw_mask))

    def __init__(self, mask: List[str]):
        self._mask = mask

    def apply(self, val: int) -> List[int]:
        value_as_list = list(f"{val:036b}")
        for idx, mask_char in enumerate(self._mask):
            if mask_char == "X":
                value_as_list[idx] = "X"
            elif mask_char == "1":
                value_as_list[idx] = "1"

        return MaskV2._generate_combinations(value_as_list)

    @staticmethod
    def _generate_combinations(value: List[str]) -> List[int]:
        results = []
        MaskV2._generate_combinations_rec(value, 0, results)
        return results

    @staticmethod
    def _generate_combinations_rec(value: List[str], index: int, results: List[int]) -> None:
        try:
            index_of_x = value.index("X", index)
            first = value.copy()
            first[index_of_x] = "0"
            MaskV2._generate_combinations_rec(first, index_of_x + 1, results)
            second = value.copy()
            second[index_of_x] = "1"
            MaskV2._generate_combinations_rec(second, index_of_x + 1, results)
        except ValueError:
            # no more X to be replaced, so store the number
            results.append(int("".join(value), 2))


def execute_program_v2(lines: Iterable[str]) -> Dict[int, int]:
    mask = MaskV2.noop()
    memory = {}
    for line in lines:
        safe_line = line.rstrip()
        if safe_line.startswith(MASK_LINE_PREFIX):
            mask = MaskV2.parse(safe_line[len(MASK_LINE_PREFIX):])
        else:
            address, value = _extract_mem_instruction(safe_line)
            addresses = mask.apply(address)
            for a in addresses:
                memory[a] = value

    return memory


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        raw_lines = list(file.readlines())

        solution_part1 = sum_memory(
            execute_program(raw_lines)
        )
        print(f"solution (part1): {solution_part1}")
        assert solution_part1 == 17028179706934

        solution_part2 = sum_memory(
            execute_program_v2(raw_lines)
        )
        print(f"solution (part2): {solution_part2}")
        assert solution_part2 == 3683236147222
