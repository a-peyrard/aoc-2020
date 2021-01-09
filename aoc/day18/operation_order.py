"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted
by the child sitting next to you. They're curious if you could help them with their math homework.
Unfortunately, it seems like this "math" follows different rules than you remember.
The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*),
and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before
 it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the
 operator, and multiplication still finds the product.
However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the
operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.
For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:
1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) +
(4 * (5 + 6)):
1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:
    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the
homework; what is the sum of the resulting values?

--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the
next section: advanced math.
Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with.
Instead, addition is evaluated before multiplication.
For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:
1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231
Here are the other examples from above:
    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
What do you get if you add up the results of evaluating the homework problems using these new rules?


"""
import os
import time
from enum import Enum
from typing import List, NamedTuple, Union, Set, Tuple, Optional


class MyEnum(Enum):
    @classmethod
    def values(cls) -> Set[str]:
        return set(map(lambda o: o.value, cls))


class Operator(MyEnum):
    ADD = "+"
    MUL = "*"

    def execute(self, a: int, b: int):
        if self == Operator.ADD:
            return a + b
        elif self == Operator.MUL:
            return a * b
        else:
            raise ValueError(f"Unknown operator: {self}")


class Ponctuation(MyEnum):
    OPEN_BRACKET = "("
    CLOSE_BRACKET = ")"


class ValueNode(NamedTuple):
    value: int


class OperatorNode(NamedTuple):
    operator: Operator
    left: Union[ValueNode, 'OperatorNode']
    right: Union[ValueNode, 'OperatorNode']


EquationTree = Union[OperatorNode, ValueNode]


def solve_equation(equation: str, priority: Optional[Operator] = None) -> int:
    return _solve_equation_tree(
        _parse_equation(
            _tokenize(equation),
            priority
        )
    )


def _parse_equation(tokens: List[str],
                    priority: Optional[Operator] = None) -> EquationTree:
    index = 0
    current = None
    current_is_protected = False
    operator = None
    while index < len(tokens):
        next_current_will_be_protected = False
        token = tokens[index]
        if isinstance(token, Operator):
            operator = token
        else:
            if isinstance(token, int):
                node = ValueNode(token)
            elif token == Ponctuation.OPEN_BRACKET:
                index, sub_list = _extract_sub_equation(index + 1, tokens)
                node = _parse_equation(sub_list, priority)
                next_current_will_be_protected = True
            else:
                raise ValueError(f"Unexpected token: {token}")

            if current:
                current_operator = _get_node_operator(current)
                if not current_is_protected and priority and current_operator and \
                        operator == priority and current_operator != priority:
                    current = OperatorNode(
                        operator=current_operator,
                        left=current.left,
                        right=OperatorNode(
                            operator=operator,
                            left=current.right,
                            right=node
                        )
                    )
                else:
                    current = OperatorNode(
                        operator=operator,
                        left=current,
                        right=node
                    )

                current_is_protected = False
            else:
                current = node
                current_is_protected = next_current_will_be_protected

        index += 1

    return current


def _get_node_operator(node: EquationTree) -> Optional[Operator]:
    if isinstance(node, OperatorNode):
        return node.operator
    return None


def _extract_sub_equation(index: int, tokens: List[str]) -> Tuple[int, List[str]]:
    sub = []
    open_brackets = 1
    while index < len(tokens):
        token = tokens[index]
        if isinstance(token, Ponctuation):
            if token == Ponctuation.OPEN_BRACKET:
                open_brackets += 1
            else:
                open_brackets -= 1
                if open_brackets == 0:
                    return index, sub
        sub.append(token)
        index += 1

    raise ValueError(f"Unable to extract a sub-equation from {tokens[index:]}")


def _tokenize(equation: str) -> List[str]:
    tokens = []
    index = 0
    operators = Operator.values()
    parenthesis = Ponctuation.values()
    while index < len(equation):
        c = equation[index]
        if c in operators:
            tokens.append(Operator(c))
        elif c.isdigit():
            number = c
            # a number might have several digits
            sub_index = index + 1
            while sub_index < len(equation):
                sub_c = equation[sub_index]
                if sub_c.isdigit():
                    number += sub_c
                else:
                    break
                sub_index += 1

            tokens.append(int(number))
            index += sub_index - index - 1
        elif c in parenthesis:
            tokens.append(Ponctuation(c))

        index += 1

    return tokens


def _solve_equation_tree(tree: EquationTree) -> int:
    if isinstance(tree, ValueNode):
        return tree.value

    a = _solve_equation_tree(tree.left)
    b = _solve_equation_tree(tree.right)

    return tree.operator.execute(a, b)


def solve_part1(equations: List[str]) -> int:
    return sum(map(solve_equation, equations))


def solve_part2(equations: List[str]) -> int:
    return sum(map(
        lambda e: solve_equation(equation=e, priority=Operator.ADD),
        equations)
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _equations = list(file.readlines())

        start = time.time()
        solution_part1 = solve_part1(_equations)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 23507031841020

        start = time.time()
        solution_part2 = solve_part2(_equations)
        end = time.time()
        print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        assert solution_part2 == 218621700997826
