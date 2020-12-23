from hamcrest import assert_that, equal_to

from aoc.day1.expense_report import calculate_expense, _three_sum


class TestCalculateExpense:
    def test_it_should_calculate_expense_for_small_example(self):
        # GIVEN
        numbers = [
            1721,
            979,
            366,
            299,
            675,
            1456
        ]

        # WHEN
        res = calculate_expense(numbers)

        # THEN
        assert_that(res, equal_to(514579))


class TestThreeSum:
    def test_it_should_find_three_sum(self):
        # GIVEN
        numbers = [1, 3, 6, 2, 8, 10, 5]

        # WHEN
        res = _three_sum(numbers, 13)

        # THEN
        assert_that(res, equal_to((1, 3, 4)))
