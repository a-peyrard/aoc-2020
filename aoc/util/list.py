from typing import TypeVar, Iterable, List

T = TypeVar("T")


def flat_map(iterable: Iterable[Iterable[T]]) -> List[T]:
    return [
        t
        for ts in iterable
        for t in ts
    ]
