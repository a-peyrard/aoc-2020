from hamcrest import assert_that, equal_to

from aoc.util.list import flat_map, count


class TestFlatMap:
    def test_should_flatten_a_list_of_list(self):
        # GIVEN
        li = [[1, 2, 3], [4, 5]]

        # WHEN
        res = flat_map(li)

        # THEN
        assert_that(res, equal_to([1, 2, 3, 4, 5]))


class TestCount:
    def test_should_count_iterable_elements(self):
        # GIVEN
        li = [True, True, False, True, True]

        # WHEN
        c = count(filter(True.__eq__, li))

        # THEN
        assert_that(c, equal_to(4))
