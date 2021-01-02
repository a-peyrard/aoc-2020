from hamcrest import assert_that, equal_to

from aoc.day14.docking_data import Mask, execute_program


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
