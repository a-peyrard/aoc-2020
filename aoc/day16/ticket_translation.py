"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is
 on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should
 probably figure out what it says before you get to the train station after the next flight.
Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure
out the fields these tickets must have and the valid ranges for values in those fields.
You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the
same train service (via the airport security cameras) together into a single document you can reference (your puzzle
input).
The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values
for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class
and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).
Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the
order they appear; every ticket has the same format. For example, consider this ticket:
.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,
303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've
extracted just the numbers in such a way that the first number is always the same specific field, the second number is
always a different specific field, and so on - you just don't know what each position actually means!
Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for
any field. Ignore your ticket for now.
For example, suppose you have the following notes:
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only
 whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket
  are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are
   are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 +
   55 + 12 = 71.
Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

"""
import os
import re
import time
from typing import List, Tuple, NamedTuple

CONSTRAINT_REGEX = re.compile(r"^(.*?): (\d+)-(\d+) or (\d+)-(\d+)$")


class Range(NamedTuple):
    min_bound: int
    max_bound: int

    def in_range(self, field: int) -> bool:
        return self.min_bound <= field <= self.max_bound


class Constraint(NamedTuple):
    name: str
    ranges: List[Range]


# define some types
Ticket = List[int]


def _parse(lines: List[str]) -> Tuple[List[Constraint], Ticket, List[Ticket]]:
    index = 0

    line = lines[index].rstrip()
    index += 1
    constraints = []
    while line:
        constraints.append(_parse_constraint(line))
        line = lines[index].rstrip()
        index += 1

    index += 1
    line = lines[index].rstrip()
    my_ticket = _parse_ticket(line)

    index += 3
    other_tickets = []
    for idx in range(index, len(lines)):
        other_tickets.append(_parse_ticket(lines[idx].rstrip()))

    return constraints, my_ticket, other_tickets


def _parse_ticket(line: str) -> Ticket:
    return list(map(int, line.split(",")))


def _parse_constraint(line: str) -> Constraint:
    matcher = CONSTRAINT_REGEX.search(line)
    if not matcher or len(matcher.groups()) != 5:
        raise ValueError(f"Unable to parse constraint: {line}")

    return Constraint(
        name=matcher.group(1),
        ranges=[
            Range(int(matcher.group(2)), int(matcher.group(3))),
            Range(int(matcher.group(4)), int(matcher.group(5)))
        ]
    )


def add_errors(tickets: List[Ticket], constraints: List[Constraint]) -> int:
    return sum((
        sum(_get_errors_in_ticket(ticket, constraints))
        for ticket in tickets
    ))


def _get_errors_in_ticket(ticket: Ticket, constraints: List[Constraint]) -> List[int]:
    return [
        field
        for field in ticket
        if not _check_field(field, constraints)
    ]


def _check_field(field: int, constraints: List[Constraint]) -> bool:
    return any(map(lambda c: _check_field_for_constraint(field, c), constraints))


def _check_field_for_constraint(field: int, constraint: Constraint) -> bool:
    return any(map(lambda r: r.in_range(field), constraint.ranges))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _constraints, _, _other_tickets = _parse(list(file.readlines()))

        start = time.time()
        solution_part1 = add_errors(_other_tickets, _constraints)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 25972
