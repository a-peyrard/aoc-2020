"""
--- Day 23: Crab Cups ---

The small crab challenges you to a game! The crab is going to mix up some cups, and you have to predict where they'll
end up.
The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were
32415, there would be five cups in the circle; going clockwise around the circle from the first cup, the cups would be
labeled 3, 2, 4, 1, 5, and then back to 3 again.
Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do
100 moves.
Each move, the crab does the following actions:
    The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the
    circle; cup spacing is adjusted as necessary to maintain the circle.
    The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would
    select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't
    just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps
    around to the highest value on any cup's label instead.
    The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep
    the same order as when they were picked up.
    The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
For example, suppose your cup labeling were 389125467. If the crab were to do merely 10 moves, the following changes
would occur:

-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6

In the above example, the cups' values are the labels as they appear moving clockwise around the circle; the current cup
 is marked with ( ).
After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels
 clockwise into a single string with no extra characters; each number except 1 should appear exactly once. In the above
 example, after 10 moves, the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374. If the crab
 were to complete all 100 moves, the order after cup 1 would be 67384529.
Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?
Your puzzle input is 538914762.

--- Part Two ---

Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab), you are quite surprised when
the crab starts arranging many cups in a circle on your raft - one million (1000000) in total.
Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing
 fashion starting from the number after the highest number in your list and proceeding one by one until one million is
 reached. (For example, if your labeling were 54321, the cups would be numbered 5, 4, 3, 2, 1, and then start counting
 up from 6 until one million is reached.) In this way, every number from one through one million is used exactly once.
After discovering where you made the mistake in translating Crab Numbers, you realize the small crab isn't going to do
merely 100 moves; the crab is going to do ten million (10000000) moves!
The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise of cup 1.
You can have them if you predict what the labels on those cups will be when the crab is finished.
In the above example (389125467), this would be 934001 and then 159792; multiplying these together produces
149245887792.
Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels
together?


"""
import time
from dataclasses import dataclass
from operator import attrgetter
from typing import Dict, List, Iterable, Set


DEBUG = False


@dataclass
class Cup:
    @staticmethod
    def parse(raw_cups: str, cups_wanted: int = -1) -> 'Cup':
        # create a linked list to store the cups
        first = Cup(value=int(raw_cups[0]))
        previous = first
        max_cup_value = -1
        for raw_cup in raw_cups[1:]:
            value = int(raw_cup)
            cur = Cup(value)
            if value > max_cup_value:
                max_cup_value = value
            previous.next = cur
            previous = cur

        for additional_cup in range(max_cup_value + 1, cups_wanted + 1):
            cur = Cup(value=additional_cup)
            previous.next = cur
            previous = cur

        # we need a circle, the last cup is linked to the first one
        previous.next = first

        return first

    value: int
    next: 'Cup' = None

    def next_cup(self, distance: int = 0) -> 'Cup':
        cur = self.next
        for _ in range(distance):
            cur = cur.next
        return cur

    def cut(self, to_cup: 'Cup') -> 'Cup':
        self.next = to_cup.next

        return self

    def insert_after(self, start_chain, end_chain) -> 'Cup':
        end_chain.next = self.next
        self.next = start_chain

        return self

    def iter(self) -> Iterable['Cup']:
        yield self
        cur = self.next
        while cur != self:
            yield cur
            cur = cur.next

    def __repr__(self) -> str:
        res = f"{self.value}"
        cur = self.next
        while cur != self:
            res += f", {cur.value}"
            cur = cur.next

        return res


class Cups:
    def __init__(self, cup: Cup):
        self._cup: Cup = cup

        self._ordered_cups: List[Cup] = \
            list(sorted(self._cup.iter(), key=lambda c: c.value, reverse=True))

        self._lookup: Dict[int, int] = {
            cup.value: idx
            for idx, cup in enumerate(self._ordered_cups)
        }

        self._number_of_cups = len(self._ordered_cups)

    def get_cup(self, cup_value: int):
        return self._ordered_cups[self._lookup[cup_value]]

    @property
    def current_cup(self):
        return self._cup

    @current_cup.setter
    def current_cup(self, new_cup):
        self._cup = new_cup

    def move_to_next_cup(self) -> 'Cups':
        self._cup = self._cup.next
        return self

    def get_lower_cup(self, value: int, disallowed_cup_values: Set[int]):
        idx = self._lookup[value]
        next_idx = (idx + 1) % self._number_of_cups
        lower_cup = self._ordered_cups[next_idx]
        while lower_cup.value in disallowed_cup_values:
            next_idx = (next_idx + 1) % self._number_of_cups
            lower_cup = self._ordered_cups[next_idx]

        return lower_cup


def generate_labels(cups: Cups) -> str:
    cup = cups.get_cup(1)
    cup_values = list(map(str, map(attrgetter("value"), cup.iter())))

    return "".join(cup_values[1:])


def play_game(cups: Cups, iterations: int = 100) -> Cups:
    for move_idx in range(iterations):
        cups = do_move(move_idx, cups)

    return cups


def do_move(move_idx: int, cups: Cups) -> Cups:
    DEBUG and print(f"""-- move {move_idx + 1} --
cups: {cups.current_cup!r}
""")
    cup = cups.current_cup
    used_cups = set()
    next_cup1 = cup.next
    used_cups.add(next_cup1.value)
    next_cup2 = next_cup1.next
    used_cups.add(next_cup2.value)
    next_cup3 = next_cup2.next
    used_cups.add(next_cup3.value)

    cup.cut(to_cup=next_cup3)
    cup_where_to_attach = cups.get_lower_cup(cup.value, disallowed_cup_values=used_cups)
    cup_where_to_attach.insert_after(
        start_chain=next_cup1,
        end_chain=next_cup3
    )
    cups.move_to_next_cup()

    return cups


def generate_prod_part2(cups: Cups) -> int:
    cup = cups.get_cup(1)
    next_1 = cup.next
    next_2 = next_1.next

    return next_1.value * next_2.value


if __name__ == "__main__":
    _input = "538914762"

    start = time.time()
    _cups = play_game(Cups(Cup.parse(_input)))
    solution_part1 = generate_labels(_cups)
    end = time.time()
    print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
    assert solution_part1 == "54327968"

    start = time.time()
    _cups = play_game(
        cups=Cups(Cup.parse(_input, cups_wanted=1000000)),
        iterations=10000000
    )
    solution_part2 = generate_prod_part2(_cups)
    end = time.time()
    print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
    assert solution_part2 == 157410423276
