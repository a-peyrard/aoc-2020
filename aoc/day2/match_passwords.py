"""
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.
The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers;
we can't log in!" You ask if you can take a look.
Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official
 Toboggan Corporate Policy that was in effect when they were chosen.
To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the
corrupted database) and the corporate policy when that password was set.
For example, suppose you have the following list:
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password. The password policy indicates the lowest and highest number
 of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must
 contain a at least 1 time and at most 3 times.
In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b,
but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of
their respective policies.
How many passwords are valid according to their policies?

"""
import os
import re
from typing import List, TypedDict


class PasswordEntry(TypedDict):
    lowest: int
    highest: int
    char: str
    password: str


def validate_passwords(passwords: List[PasswordEntry]) -> int:
    return sum(map(_validate_password, passwords))


def _validate_password(password: PasswordEntry) -> bool:
    counter = 0
    for _, char in enumerate(password["password"]):
        if char == password["char"]:
            counter += 1
            if counter > password["highest"]:
                return False

    return counter >= password["lowest"]


RAW_PASSWORD_REGEX = re.compile(r"^(\d+)-(\d+) (\w): (.*)")


def _parse_raw_password_item(item: str) -> PasswordEntry:
    matcher = RAW_PASSWORD_REGEX.search(item)
    if matcher and len(matcher.groups()) == 4:
        return {
            "lowest": int(matcher.group(1)),
            "highest": int(matcher.group(2)),
            "char": matcher.group(3),
            "password": matcher.group(4),
        }

    raise ValueError(f"Unable to extract a password entry from string '{item}'!")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as f:
        input_passwords = [
            _parse_raw_password_item(line)
            for line in f.readlines()
            if line
        ]

        solution = validate_passwords(input_passwords)
        print(f"solution (part1): {solution}")
