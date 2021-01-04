from hamcrest import equal_to, assert_that

from aoc.day16.ticket_translation import _parse, Range, Constraint, add_errors


class TestParse:
    def test_should_parse_first_example(self):
        # GIVEN
        raw = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

        # WHEN
        constraints, my_ticket, other_tickets = \
            _parse(raw.splitlines(keepends=True))

        # THEN
        assert_that(
            constraints,
            equal_to([
                Constraint("class", [Range(1, 3), Range(5, 7)]),
                Constraint("row", [Range(6, 11), Range(33, 44)]),
                Constraint("seat", [Range(13, 40), Range(45, 50)])
            ])
        )
        assert_that(
            my_ticket,
            equal_to([7, 1, 14])
        )
        assert_that(
            other_tickets,
            equal_to([
                [7, 3, 47],
                [40, 4, 50],
                [55, 2, 20],
                [38, 6, 12]
            ])
        )


class TestAddErrors:
    def test_should_validate_given_example(self):
        # GIVEN
        raw = """class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50

        your ticket:
        7,1,14

        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12"""
        constraints, _, other_tickets = \
            _parse(raw.splitlines(keepends=True))

        # WHEN
        errors = add_errors(other_tickets, constraints)

        # THEN
        assert_that(errors, equal_to(71))
