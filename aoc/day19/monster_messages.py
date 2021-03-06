"""
--- Day 19: Monster Messages ---

You land in an airport surrounded by dense forest. As you walk to your high-speed train, the Elves at the Mythical
Information Bureau contact you again. They think their satellite has collected an image of a sea monster! Unfortunately,
 the connection to the satellite is having problems, and many of the messages sent back from the satellite have been
 corrupted.
They sent you a list of the rules valid messages should obey and a list of received messages they've collected so far
(your puzzle input).
The rules for valid messages (the top part of your puzzle input) are numbered and build upon each other. For example:
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
Some rules, like 3: "b", simply match a single character (in this case, b).
The remaining rules list the sub-rules that must be followed; for example, the rule 0: 1 2 means that to match rule 0,
the text being checked must match rule 1, and the text after the part that matched rule 1 must then match rule 2.
Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means that at least one list of
sub-rules must match. (The ones that match might be different each time the rule is encountered.) For example, the rule
2: 1 3 | 3 1 means that to match rule 2, the text being checked must match rule 1 followed by rule 3 or it must match
rule 3 followed by rule 1.
Fortunately, there are no loops in the rules, so the list of possible matches will be finite. Since rule 1 matches a and
 rule 3 matches b, rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.
Here's a more interesting example:
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that are the same (aa or bb), and rule
3 matches two letters that are different (ab or ba).
Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs of letters, one pair with matching
 letters and one pair with different letters. This leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa,
  or babb.
Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then b (rule 5): aaaabb, aaabab,
abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.
The received messages (the bottom part of your puzzle input) need to be checked against the rules so you can determine
which are valid and which are corrupted. Including the rules and the messages together, this might look like:
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
Your goal is to determine the number of messages that completely match rule 0. In the above example, ababbb and abbbab
match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2. The whole message must match all of rule 0; there
 can't be extra unmatched characters in the message. (For example, aaaabbb might appear to match rule 0 above, but it
 has an extra unmatched b on the end.)
How many messages completely match rule 0?

--- Part Two ---

As you look over the list of messages, you realize your matching rules aren't quite right. To fix them, completely
replace rules 8: 42 and 11: 42 31 with the following:
8: 42 | 42 8
11: 42 31 | 42 11 31
This small change has a big impact: now, the rules do contain loops, and the list of messages they could hypothetically
match is infinite. You'll need to determine how these changes affect which messages are valid.
Fortunately, many of the rules are unaffected by this change; it might help to start by looking at which rules always
match the same set of values and how those rules (especially rules 42 and 31) are used by the new versions of rules 8
and 11.
(Remember, you only need to handle the rules you have; building a solution that could handle any hypothetical
combination of rules would be significantly more difficult.)
For example:
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba

Without updating rules 8 and 11, these rules only match three messages: bbabbbbaabaabba, ababaaaaaabaaab, and
ababaaaaabbbaba.
However, after updating rules 8 and 11, a total of 12 messages match:
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
After updating rules 8 and 11, how many messages completely match rule 0?

"""
import os
import re
import sys
import time
from typing import List, Union, Tuple, Dict, Iterable, Set

SubRule = List[List[int]]
Matcher = str
Rule = Union[SubRule, Matcher]
Rules = Dict[int, Rule]


DEBUG = False


RULE_REGEX = re.compile(r"(\d+): (.*)")
RULE_MATCHER_REGEX = re.compile(r"\"(\w+)\"")


class Node:
    def __init__(self, string: str):
        self._str = string
        self._children: List['Node'] = []

    def add_children(self, children_to_add: Iterable['Node'], visited: Set[int] = None) -> 'Node':
        self._add_children_rec(children_to_add, set() if visited is None else visited)
        return self

    def _add_children_rec(self,
                          children_to_add: Iterable['Node'],
                          visited: Set[int]) -> None:
        # avoid cycles, because we are adding the same node to multiple parents,
        # so later we want to avoid to add node to itself
        self_id = id(self)
        if self_id in visited:
            return

        visited.add(self_id)

        if self._children:
            for child in self._children:
                child._add_children_rec(children_to_add, visited)
        else:
            self._children.extend(children_to_add)

    def add_child(self, child_to_add: 'Node') -> 'Node':
        self.add_children([child_to_add])
        return self

    def validate(self, msg: str):
        return self._validate_rec(
            msg=msg,
            start_at=0,
            msg_length=len(msg)
        )

    # noinspection PyProtectedMember
    def _validate_rec(self, msg: str, start_at: int, msg_length: int):
        if start_at >= msg_length:
            return False

        if not self._validate_char(msg[start_at]):
            return False

        if start_at == msg_length - 1 and not self._children:
            return True

        next_index = start_at + 1
        return any(map(
            lambda child: child._validate_rec(msg, next_index, msg_length),
            self._children
        ))

    def _validate_char(self, char: str) -> bool:
        return char == self._str

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False

        if self._str != o._str:
            return False

        if len(self._children) != len(o._children):
            return False

        return all(
            (
                child.__eq__(o._children[index])
                for index, child in enumerate(self._children)
            )
        )

    def __repr__(self) -> str:
        return f"{id(self)}[{len(self._children)}]"


class Automaton:
    def __init__(self):
        self._starting_nodes: List[Node] = []

    def add_starting_node(self, node: Node):
        self._starting_nodes.append(node)

    def validate(self, msg: str) -> bool:
        return any(map(
            lambda node: node.validate(msg),
            self._starting_nodes
        ))


def _parse(lines: List[str]) -> Tuple[Rules, List[str]]:
    raw_rules = []
    index = 0
    line = lines[index].rstrip()
    while line:
        raw_rules.append(line)
        index += 1
        line = lines[index].rstrip()

    rules = _parse_rules(raw_rules)

    return rules, list(map(str.rstrip, lines[index:]))


def _parse_rules(raw_rules: List[str]) -> Rules:
    rules = {}
    for raw_rule in raw_rules:
        rule_idx, rule = _parse_rule_line(raw_rule)
        rules[rule_idx] = rule

    return rules


def _parse_rule_line(raw_rule_line) -> Tuple[int, Rule]:
    matcher = RULE_REGEX.search(raw_rule_line)
    if not matcher or len(matcher.groups()) != 2:
        raise ValueError(f"Unable to extract rule from {raw_rule_line}")

    return int(matcher.group(1)), _parse_rule(matcher.group(2))


def _parse_rule(raw_rule) -> Rule:
    matcher = RULE_MATCHER_REGEX.search(raw_rule)
    if matcher:
        return matcher.group(1)

    return list(
        map(
            lambda sub_rule: list(
                map(
                    int,
                    sub_rule.split()
                )
            ),
            map(
                str.strip,
                raw_rule.split("|")
            )
        )
    )


def solve_part1(messages: List[str], rules: Rules, rule_idx: int) -> int:
    automaton = _build_automaton(rules, rule_idx)
    return sum(
        map(
            automaton.validate,
            messages
        )
    )


def _build_automaton(rules: Rules,
                     rule_idx: int,
                     circuit_breaker: int = sys.maxsize) -> Automaton:
    automaton = Automaton()
    if rule_idx not in rules:
        raise ValueError(f"Unable to find rule: {rule_idx}")

    for node in _build_nodes(rule_idx, rules, circuit_breaker):
        automaton.add_starting_node(node)

    return automaton


def _build_nodes(rule_idx: int,
                 rules: Rules,
                 circuit_breaker: int = sys.maxsize,
                 depth: int = 0) -> List[Node]:
    if depth > circuit_breaker:
        # break the circuit, so return a not used character, like that this path
        # will never match anything...
        DEBUG and print(f"{_depth_prefix(depth)} BREAK {rule_idx} - depth {depth} > circuit breaker {circuit_breaker}")
        return [Node("@")]

    DEBUG and print(f"{_depth_prefix(depth)} build nodes from rule {rule_idx} ({rules[rule_idx]})")
    rule = rules[rule_idx]
    if isinstance(rule, str):
        result = [Node(rule)]
        DEBUG and print(f"{_depth_prefix(depth)} from rule {rule_idx} built {result}")
        return result

    result = [
        node
        for redirects in rule
        for node in _build_nodes_from_redirects(redirects, rules, circuit_breaker, depth)
    ]
    DEBUG and print(f"{_depth_prefix(depth)} built {result}")
    return result


def _build_nodes_from_redirects(redirects: List[int],
                                rules: Rules,
                                circuit_breaker: int,
                                depth: int) -> List[Node]:
    roots = _build_nodes(redirects[0], rules, circuit_breaker, depth + 1)
    current_nodes = roots
    for redirect in redirects[1:]:
        sub_nodes = _build_nodes(redirect, rules, circuit_breaker, depth + 1)
        visited = set()
        for current_node in current_nodes:
            current_node.add_children(sub_nodes, visited)

    return roots


def _depth_prefix(depth: int) -> str:
    return "    " * depth


def _patch_rules(rules: Rules) -> Rules:
    new_rules = rules.copy()
    new_rules[8] = [[42], [42, 8]]
    new_rules[11] = [[42, 31], [42, 11, 31]]
    return new_rules


def _max_message_length(messages: List[str]) -> int:
    return max(map(len, messages))


def solve_part2(messages: List[str], rules: Rules, rule_idx: int) -> bool:
    rules = _patch_rules(rules)
    max_message_length = _max_message_length(messages)
    automaton = _build_automaton(rules, rule_idx, max_message_length)
    return sum(
        map(
            automaton.validate,
            messages
        )
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _rules, _messages = _parse(list(file.readlines()))

        start = time.time()
        solution_part1 = solve_part1(_messages, _rules, rule_idx=0)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 102

        start = time.time()
        solution_part2 = solve_part2(_messages, _rules, rule_idx=0)
        end = time.time()
        print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        assert solution_part2 == 318
