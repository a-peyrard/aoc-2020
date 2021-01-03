from hamcrest import assert_that, equal_to, contains_inanyorder

from aoc.day14.docking_data import Mask, execute_program, MaskV2, execute_program_v2, sum_memory


class TestMask:
    def test_should_apply_mask(self):
        # GIVEN
        raw_mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"

        # WHEN
        mask = Mask.parse(raw_mask)
        eleven = mask.apply(11)
        one_o_one = mask.apply(101)
        zero = mask.apply(0)

        # THEN
        assert_that(eleven, equal_to(73))
        assert_that(one_o_one, equal_to(101))
        assert_that(zero, equal_to(64))

    def test_should_apply_noop_mask(self):
        # GIVEN
        mask = Mask.noop()

        # WHEN
        eleven = mask.apply(11)
        one_o_one = mask.apply(101)
        zero = mask.apply(0)

        # THEN
        assert_that(eleven, equal_to(11))
        assert_that(one_o_one, equal_to(101))
        assert_that(zero, equal_to(0))


class TestExecuteProgram:
    def test_should_validate_first_example(self):
        # GIVEN
        raw_program = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

        # WHEN
        mem = execute_program(raw_program.splitlines(keepends=True))

        # THEN
        assert_that(mem, equal_to({
            8: 64,
            7: 101
        }))

    def test_should_validate_another_example(self):
        # GIVEN
        raw_program = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1
mem[9] = 12
mem[6] = 4"""

        # WHEN
        mem = execute_program(raw_program.splitlines(keepends=True))

        # THEN
        assert_that(mem, equal_to({
            9: 13,
            6: 5
        }))

    def test_should_validate_multiple_masks_example(self):
        # GIVEN
        raw_program = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1
mem[9] = 12
mem[6] = 4"""

        # WHEN
        mem = execute_program(raw_program.splitlines(keepends=True))

        # THEN
        assert_that(mem, equal_to({
            8: 64,
            7: 101,
            9: 13,
            6: 5
        }))


class TestGenerateCombinations:
    def test_should_generate_unique_number_if_no_x(self):
        # GIVEN
        value = list("000000000000000000000000000000111011")

        # WHEN
        combinations = MaskV2._generate_combinations(value)

        # THEN
        assert_that(combinations, equal_to([59]))

    def test_should_validate_first_example(self):
        # GIVEN
        value = list("000000000000000000000000000000X1101X")

        # WHEN
        combinations = MaskV2._generate_combinations(value)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            combinations,
            contains_inanyorder(26, 27, 58, 59)
        )

    def test_should_validate_second_example(self):
        # GIVEN
        value = list("00000000000000000000000000000001X0XX")

        # WHEN
        combinations = MaskV2._generate_combinations(value)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            combinations,
            contains_inanyorder(16, 17, 18, 19, 24, 25, 26, 27)
        )


class TestMaskV2:
    def test_should_apply_first_example(self):
        # GIVEN
        mask = MaskV2.parse("000000000000000000000000000000X1001X")

        # WHEN
        results = mask.apply(42)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            results,
            contains_inanyorder(26, 27, 58, 59)
        )

    def test_should_apply_second(self):
        # GIVEN
        mask = MaskV2.parse("00000000000000000000000000000000X0XX")

        # WHEN
        results = mask.apply(26)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            results,
            contains_inanyorder(16, 17, 18, 19, 24, 25, 26, 27)
        )


class TestExecuteProgramV2:
    def test_should_validate_first_example(self):
        # GIVEN
        raw_program = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

        # WHEN
        mem = execute_program_v2(raw_program.splitlines(keepends=True))

        # THEN
        assert_that(sum_memory(mem), equal_to(208))
