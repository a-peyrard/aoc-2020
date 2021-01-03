"""
--- Day 15: Rambunctious Recitation ---
You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights
 have been cancelled, but a route is available to get around the storm. You take it.
While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a memory
game and are ever so excited to explain the rules!
In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers
(your puzzle input). Then, each turn consists of considering the most recently spoken number:
    If that was the first time the number has been spoken, the current player says 0.
    Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from
    when it was previously spoken.
So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or
an age (if the last number is a repeat).
For example, suppose the starting numbers are 0,3,6:
    Turn 1: The 1st number spoken is a starting number, 0.
    Turn 2: The 2nd number spoken is a starting number, 3.
    Turn 3: The 3rd number spoken is a starting number, 6.
    Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number had been spoken, the 4th
    number spoken is 0.
    Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, the next number to speak is
     the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the
     time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
    Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number
    spoken is 5 - 2, 3.
    Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
    Turn 8: Since 1 is new, the 8th number spoken is 0.
    Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
    Turn 10: 4 is new, so the 10th number spoken is 0.
(The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)
Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be
 436.
Here are a few more examples:
    Given the starting numbers 1,3,2, the 2020th number spoken is 1.
    Given the starting numbers 2,1,3, the 2020th number spoken is 10.
    Given the starting numbers 1,2,3, the 2020th number spoken is 27.
    Given the starting numbers 2,3,1, the 2020th number spoken is 78.
    Given the starting numbers 3,2,1, the 2020th number spoken is 438.
    Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
Given your starting numbers, what will be the 2020th number spoken?

"""
import time
from collections import defaultdict
from typing import List, Tuple, Optional, DefaultDict


class History:
    def __init__(self):
        self._last_seen: Optional[int] = None
        self._before_last_seen: Optional[int] = None

    def seen_at(self, turn_idx) -> None:
        self._before_last_seen = self._last_seen
        self._last_seen = turn_idx

    def time_since_last_seen(self) -> int:
        if self._before_last_seen is None:
            return 0
        else:
            return self._last_seen - self._before_last_seen


def _init(starting_numbers: List[int]) -> Tuple[int, int, DefaultDict[int, History]]:
    memo = defaultdict(lambda: History())
    last_spoken_number = 0
    for idx, starting_number in enumerate(starting_numbers):
        memo[starting_number].seen_at(idx + 1)
        last_spoken_number = starting_number

    return last_spoken_number, len(starting_numbers), memo


def play_game(starting_numbers: List[int], number_of_turns: int) -> int:
    if number_of_turns <= len(starting_numbers):
        return starting_numbers[number_of_turns - 1]

    last_spoken_number, last_turn, memo = _init(starting_numbers)
    for turn_index in range(last_turn + 1, number_of_turns + 1):
        last_spoken_number = memo[last_spoken_number].time_since_last_seen()
        memo[last_spoken_number].seen_at(turn_index)

    return last_spoken_number


if __name__ == "__main__":
    start = time.time()
    solution_part1 = play_game([18, 11, 9, 0, 5, 1], 2020)
    end = time.time()
    print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
    assert solution_part1 == 959

    start = time.time()
    solution_part2 = play_game([18, 11, 9, 0, 5, 1], 30000000)
    end = time.time()
    print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
    assert solution_part2 == 116590
