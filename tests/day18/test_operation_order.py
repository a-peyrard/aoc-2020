from hamcrest import equal_to, assert_that

from aoc.day18.operation_order import solve_equation, OperatorNode, Operator, ValueNode, _solve_equation_tree, \
    _parse_equation, _tokenize, Ponctuation


class TestSolveEquation:
    def test_should_solve_simple_addition(self):
        # GIVEN
        equation = "1 + 2"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(3))

    def test_should_solve_simple_multiplication(self):
        # GIVEN
        equation = "2 * 3"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(6))

    def test_should_solve_simple_multiple_operations(self):
        # GIVEN
        equation = "1 + 2 * 3"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(9))

    def test_should_solve_simple_multiple_operations_with_parenthesis(self):
        # GIVEN
        equation = "1 + (2 * 3)"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(7))

    def test_should_solve_first_given_equation(self):
        # GIVEN
        equation = "1 + 2 * 3 + 4 * 5 + 6"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(71))

    def test_should_solve_second_given_equation(self):
        # GIVEN
        equation = "1 + (2 * 3) + (4 * (5 + 6))"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(51))

    def test_should_solve_third_given_equation(self):
        # GIVEN
        equation = "2 * 3 + (4 * 5)"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(26))

    def test_should_solve_fourth_given_equation(self):
        # GIVEN
        equation = "5 + (8 * 3 + 9 + 3 * 4 * 3)"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(437))

    def test_should_solve_fifth_given_equation(self):
        # GIVEN
        equation = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(12240))

    def test_should_solve_sixth_given_equation(self):
        # GIVEN
        equation = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(13632))


class TestSolveEquationPart2:
    def test_should_solve_simple_addition(self):
        # GIVEN
        equation = "1 + 2"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(3))

    def test_should_solve_simple_multiplication(self):
        # GIVEN
        equation = "2 * 3"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(6))

    def test_should_solve_simple_multiple_operations(self):
        # GIVEN
        equation = "1 + 2 * 3"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(9))

    def test_should_solve_simple_multiple_operations_with_parenthesis(self):
        # GIVEN
        equation = "1 + (2 * 3)"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(7))

    def test_should_solve_give_priority_to_addition(self):
        # GIVEN
        equation = "2 * 1 + 4"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(10))

    def test_should_solve_first_given_equation(self):
        # GIVEN
        equation = "1 + 2 * 3 + 4 * 5 + 6"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(231))

    def test_should_solve_second_given_equation(self):
        # GIVEN
        equation = "1 + (2 * 3) + (4 * (5 + 6))"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(51))

    def test_should_solve_third_given_equation(self):
        # GIVEN
        equation = "2 * 3 + (4 * 5)"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(46))

    def test_should_solve_fourth_given_equation(self):
        # GIVEN
        equation = "5 + (8 * 3 + 9 + 3 * 4 * 3)"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(1445))

    def test_should_solve_sub_fourth_given_equation(self):
        # GIVEN
        equation = "8 * 3 + 9 + 3 * 4 * 3"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(1440))

    def test_should_solve_fifth_given_equation(self):
        # GIVEN
        equation = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(669060))

    def test_should_solve_sub1_from_fifth_given_equation(self):
        # GIVEN
        equation = "3 + (8 + 6 * 4)"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(59))

    def test_should_solve_sub2_from_fifth_given_equation(self):
        # GIVEN
        equation = "9 * 3 + (50 + 6)"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(531))

    def test_should_solve_sixth_given_equation(self):
        # GIVEN
        equation = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(23340))

    def test_should_solve_sub_1_from_sixth_given_equation(self):
        # GIVEN
        equation = "(6 + 9 * 8 + 6) + 6"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(216))

    def test_should_solve_sub_2_from_sixth_given_equation(self):
        # GIVEN
        equation = "6 + 9 * 8 + 6"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(210))

    def test_should_solve_sub3_from_sixth_given_equation(self):
        # GIVEN
        equation = "(2 + 4 * 9) * (6 + 9 * 8 + 6) + 6"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(11664))

    def test_should_solve_derived_from_sub3_from_sixth_given_equation(self):
        # GIVEN
        equation = "4 * (2 + 2) + 6"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(40))


    def test_should_solve_sub4_from_sixth_given_equation(self):
        # GIVEN
        equation = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2"

        # WHEN
        result = solve_equation(equation, priority=Operator.ADD)

        # THEN
        assert_that(result, equal_to(11666))

    def test_should_solve_with_parenthesis_before_addition(self):
        # GIVEN
        equation = "(9 * 8) + 6"

        # WHEN
        result = solve_equation(equation)

        # THEN
        assert_that(result, equal_to(78))


class TestParseEquation:
    def test_should_parse_simple_addition(self):
        # GIVEN
        equation = "1 + 2"

        # WHEN
        tree = _parse_equation(_tokenize(equation))

        # THEN
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.ADD,
                    left=ValueNode(1),
                    right=ValueNode(2)
                )
            )
        )

    def test_should_parse_simple_multiplication(self):
        # GIVEN
        equation = "1 * 2"

        # WHEN
        tree = _parse_equation(_tokenize(equation))

        # THEN
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.MUL,
                    left=ValueNode(1),
                    right=ValueNode(2)
                )
            )
        )

    def test_should_parse_numbers_with_multiple_digits(self):
        # GIVEN
        equation = "123 + 456"

        # WHEN
        tree = _parse_equation(_tokenize(equation))

        # THEN
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.ADD,
                    left=ValueNode(123),
                    right=ValueNode(456)
                )
            )
        )

    def test_should_parse_ponctuation(self):
        # GIVEN
        equation = "1 + (2 * 3)"

        # WHEN
        tree = _parse_equation(_tokenize(equation))

        # THEN
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.ADD,
                    left=ValueNode(1),
                    right=OperatorNode(
                        operator=Operator.MUL,
                        left=ValueNode(2),
                        right=ValueNode(3)
                    )
                )
            )
        )

    def test_should_parse_with_priority(self):
        # GIVEN
        equation = "2 * 1 + 4"

        # WHEN
        tree = _parse_equation(_tokenize(equation), priority=Operator.ADD)

        # THEN
        #   *
        #  / \
        # 2   +
        #    / \
        #   1   4
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.MUL,
                    left=ValueNode(2),
                    right=OperatorNode(
                        operator=Operator.ADD,
                        left=ValueNode(1),
                        right=ValueNode(4)
                    )
                )
            )
        )

    def test_should_parse_with_priority_more_complex_equation(self):
        # GIVEN
        equation = "2 * 1 + 4 + 3"

        # WHEN
        tree = _parse_equation(_tokenize(equation), priority=Operator.ADD)

        # THEN
        #   *
        #  / \
        # 2   +
        #    / \
        #   +   3
        #  / \
        # 1   4
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.MUL,
                    left=ValueNode(2),
                    right=OperatorNode(
                        operator=Operator.ADD,
                        left=OperatorNode(
                            operator=Operator.ADD,
                            left=ValueNode(1),
                            right=ValueNode(4)
                        ),
                        right=ValueNode(3)
                    )
                )
            )
        )

    def test_should_parse_and_give_priority_to_parenthesis_even_with_forced_priorities(self):
        # GIVEN
        equation = "5 + (8 * 3)"

        # WHEN
        tree = _parse_equation(_tokenize(equation), priority=Operator.ADD)

        # THEN
        #   +
        #  / \
        # 5   *
        #    / \
        #   8   3
        assert_that(
            tree,
            equal_to(
                OperatorNode(
                    operator=Operator.ADD,
                    left=ValueNode(5),
                    right=OperatorNode(
                        operator=Operator.MUL,
                        left=ValueNode(8),
                        right=ValueNode(3)
                    )
                )
            )
        )


class TestTokenize:
    def test_should_tokenize_simple_addition(self):
        # GIVEN
        equation = "1 + 2"

        # WHEN
        tokens = _tokenize(equation)

        # THEN
        assert_that(
            tokens,
            equal_to([
                1,
                Operator.ADD,
                2
            ])
        )

    def test_should_tokenize_numbers_with_multiple_digits(self):
        # GIVEN
        equation = "123 + 456"

        # WHEN
        tokens = _tokenize(equation)

        # THEN
        assert_that(
            tokens,
            equal_to([
                123,
                Operator.ADD,
                456
            ])
        )

    def test_should_tokenize_more_complex_equations(self):
        # GIVEN
        equation = "((2 + 4 * 9) * (42 + 9) + 3) * 21"

        # WHEN
        tokens = _tokenize(equation)

        # THEN
        assert_that(
            tokens,
            equal_to([
                Ponctuation.OPEN_BRACKET,
                Ponctuation.OPEN_BRACKET,
                2,
                Operator.ADD,
                4,
                Operator.MUL,
                9,
                Ponctuation.CLOSE_BRACKET,
                Operator.MUL,
                Ponctuation.OPEN_BRACKET,
                42,
                Operator.ADD,
                9,
                Ponctuation.CLOSE_BRACKET,
                Operator.ADD,
                3,
                Ponctuation.CLOSE_BRACKET,
                Operator.MUL,
                21
            ])
        )


class TestSolveEquationTree:
    def test_should_solve_simple_addition_tree(self):
        # GIVEN
        tree = OperatorNode(
            operator=Operator.ADD,
            left=ValueNode(1),
            right=ValueNode(2)
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(3)
        )

    def test_should_solve_simple_multiplication_tree(self):
        # GIVEN
        tree = OperatorNode(
            operator=Operator.MUL,
            left=ValueNode(3),
            right=ValueNode(2)
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(6)
        )

    def test_should_solve_simple_equation(self):
        # GIVEN
        #      *
        #     / \
        #    +   3
        #   / \
        #  1   2
        tree = OperatorNode(
            operator=Operator.MUL,
            left=OperatorNode(
                operator=Operator.ADD,
                left=ValueNode(1),
                right=ValueNode(2)
            ),
            right=ValueNode(3)
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(9)
        )

    def test_should_solve_another_simple_equation(self):
        # GIVEN
        #        *
        #     /     \
        #    +       +
        #   / \     / \
        #  1   2   4   5
        tree = OperatorNode(
            operator=Operator.MUL,
            left=OperatorNode(
                operator=Operator.ADD,
                left=ValueNode(1),
                right=ValueNode(2)
            ),
            right=OperatorNode(
                operator=Operator.ADD,
                left=ValueNode(4),
                right=ValueNode(5)
            )
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(27)
        )

    def test_should_solve_again_another_equation(self):
        # GIVEN: 1 + (2 * 3)
        #      +
        #     / \
        #    1   *
        #       / \
        #      2   3
        tree = OperatorNode(
            operator=Operator.ADD,
            left=ValueNode(1),
            right=OperatorNode(
                operator=Operator.MUL,
                left=ValueNode(2),
                right=ValueNode(3)
            )
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(7)
        )

    def test_should_solve_priority_tree(self):
        # GIVEN: 2 * 1 + 4
        #   *
        #  / \
        # 2   +
        #    / \
        #   1   4
        tree = OperatorNode(
            operator=Operator.MUL,
            left=ValueNode(2),
            right=OperatorNode(
                operator=Operator.ADD,
                left=ValueNode(1),
                right=ValueNode(4)
            )
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(10)
        )

    def test_should_solve_with_parenthesis_and_priorities(self):
        # GIVEN: 5 + (8 * 3)
        #   +
        #  / \
        # 5   *
        #    / \
        #   8   3
        tree = OperatorNode(
            operator=Operator.ADD,
            left=ValueNode(5),
            right=OperatorNode(
                operator=Operator.MUL,
                left=ValueNode(8),
                right=ValueNode(3)
            )
        )

        # WHEN
        result = _solve_equation_tree(tree)

        # THEN
        assert_that(
            result,
            equal_to(29)
        )
