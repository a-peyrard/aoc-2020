import os
import time
from collections import deque
from functools import reduce
from itertools import islice
from math import prod
from typing import Tuple, Iterable, Deque

from aoc.util.text import generate_paragraphs


Deck = Deque[int]


def _parse(lines: Iterable[str]) -> Tuple[Deck, Deck]:
    raw_decks = generate_paragraphs(lines)
    return _parse_deck(next(raw_decks)), _parse_deck(next(raw_decks))


def _parse_deck(lines: Iterable[str]) -> Deck:
    iterator = iter(lines)
    next(iterator)

    cards = list(map(int, iterator))
    return deque(cards, maxlen=len(cards) * 2)


def game(player1, player2, recursive):
    seen = set()

    while player1 and player2:
        if (state := (tuple(player1), tuple(player2))) in seen:
            return True, player1
        seen.add(state)

        (card1, *player1), (card2, *player2) = player1, player2

        if recursive and len(player1) >= card1 and len(player2) >= card2:
            player1win = game(
                player1[:card1],
                player2[:card2],
                recursive
            )[0]
        else:
            player1win = card1 > card2

        if player1win:
            player1.extend((card1, card2))
        else:
            player2.extend((card2, card1))

    return (True, player1) if player1 else (False, player2)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _deck1, _deck2 = _parse(file.readlines())

        for _recursive in False, True:
            start = time.time()
            player = game(list(_deck1), list(_deck2), _recursive)[1]
            solution = sum(map(prod, enumerate(reversed(player), 1)))
            end = time.time()
            print(f"solution (part{_recursive}) {solution} in {(end - start) * 1000}ms")

        # start = time.time()
        # solution_part1 = play_game(_deck1.copy(), _deck2.copy())
        # end = time.time()
        # print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        # assert solution_part1 == 32413
        #
        # start = time.time()
        # solution_part2 = play_recurse_game(_deck1.copy(), _deck2.copy())
        # end = time.time()
        # print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        # assert solution_part2 == 31596
