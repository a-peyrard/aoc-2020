from hamcrest import assert_that, equal_to

from aoc.day8.handheld_halting import play_instructions, _parse, fix_program


class TestPlayInstructions:
    def test_should_validate_given_example(self):
        # GIVEN
        instructions = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

        # WHEN
        res, _ = play_instructions(
            _parse(instructions.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(5))


class TestFixProgram:
    def test_should_validate_given_example(self):
        # GIVEN
        instructions = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

        # WHEN
        res = fix_program(
            _parse(instructions.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(8))
