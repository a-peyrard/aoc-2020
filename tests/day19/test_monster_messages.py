from hamcrest import equal_to, assert_that, contains_exactly, contains_inanyorder

from aoc.day19.monster_messages import _parse_rules, _build_automaton, Node, _build_nodes


class TestAutomaton:
    def test_should_validate_first_given_example(self):
        # GIVEN
        raw_rules = """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate_aab = automaton.validate("aab")
        validate_aba = automaton.validate("aba")
        dont_validate_a = automaton.validate("a")
        dont_validate_b = automaton.validate("b")
        dont_validate_aa = automaton.validate("aa")

        # THEN
        assert_that(validate_aab, equal_to(True))
        assert_that(validate_aba, equal_to(True))
        assert_that(dont_validate_a, equal_to(False))
        assert_that(dont_validate_b, equal_to(False))
        assert_that(dont_validate_aa, equal_to(False))

    def test_should_validate_second_example_msg1(self):
        # GIVEN
        #
        # a a a a b b
        # a a a b a b
        # a b b a b b
        # a b b b a b
        # a a b a a b
        # a b a a a b
        # a a b b b b
        # a b a b b b
        #
        raw_rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate = automaton.validate("ababbb")

        # THEN
        assert_that(validate, equal_to(True))

    def test_should_validate_second_example_msg2(self):
        # GIVEN
        raw_rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate = automaton.validate("bababa")

        # THEN
        assert_that(validate, equal_to(False))

    def test_should_validate_second_example_msg3(self):
        # GIVEN
        raw_rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate = automaton.validate("abbbab")

        # THEN
        assert_that(validate, equal_to(True))

    def test_should_validate_second_example_msg4(self):
        raw_rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate = automaton.validate("aaabbb")

        # THEN
        assert_that(validate, equal_to(False))

    def test_should_validate_second_example_msg5(self):
        # GIVEN
        raw_rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
        automaton = _build_automaton(_parse_rules(raw_rules.splitlines()), rule_idx=0)

        # WHEN
        validate = automaton.validate("aaaabbb")

        # THEN
        assert_that(validate, equal_to(False))


class TestNodeWithoutChildren:
    def test_should_validate_matching_single_character_message(self):
        # GIVEN
        node = Node("a")

        # WHEN
        validate = node.validate("a")

        # THEN
        assert_that(validate, equal_to(True))

    def test_should_not_validate_not_matching_single_character_message(self):
        # GIVEN
        node = Node("a")

        # WHEN
        validate = node.validate("z")

        # THEN
        assert_that(validate, equal_to(False))

    def test_should_not_validate_multiple_character_message_even_starting_with_character(self):
        # GIVEN
        node = Node("a")

        # WHEN
        validate = node.validate("ab")

        # THEN
        assert_that(validate, equal_to(False))

    def test_should_not_validate_multiple_character_message(self):
        # GIVEN
        node = Node("a")

        # WHEN
        validate = node.validate("ba")

        # THEN
        assert_that(validate, equal_to(False))


class TestNodeWithChildren:
    def test_should_validate_matching_two_characters_message(self):
        # GIVEN
        node = Node("a")\
            .add_child(Node("b"))

        # WHEN
        validate = node.validate("ab")

        # THEN
        assert_that(validate, equal_to(True))

    def test_should_not_validate_not_matching_two_characters_message(self):
        # GIVEN
        node = Node("a")\
            .add_child(Node("b"))

        # WHEN
        validate = node.validate("ac")

        # THEN
        assert_that(validate, equal_to(False))

    def test_should_validate_multiple_second_characters_allowed_if_matching(self):
        # GIVEN
        node = Node("a").add_children([
            Node("b"),
            Node("a")
        ])

        # WHEN
        validate_ab = node.validate("ab")
        validate_aa = node.validate("aa")

        # THEN
        assert_that(validate_ab, equal_to(True))
        assert_that(validate_aa, equal_to(True))

    def test_should_not_validate_multiple_second_characters_allowed_if_not_matching(self):
        # GIVEN
        node = Node("a") \
            .add_child(Node("b")) \
            .add_child(Node("a"))

        # WHEN
        validate_ba = node.validate("ba")
        validate_bb = node.validate("bb")

        # THEN
        assert_that(validate_ba, equal_to(False))
        assert_that(validate_bb, equal_to(False))

    def test_should_not_validate_if_message_too_short(self):
        # GIVEN
        node = Node("a")\
            .add_child(Node("b"))\
            .add_child(Node("a"))

        # WHEN
        validate = node.validate("a")

        # THEN
        assert_that(validate, equal_to(False))


class TestBuildNodes:
    def test_should_build_single_character_rule(self):
        # GIVEN
        rules = {0: "a"}

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("a")
            )
        )

    def test_should_build_redirection_rule(self):
        # GIVEN
        rules = {
            0: [[1, 2]],
            1: "a",
            2: "b"
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("a").add_child(Node("b"))
            )
        )

    def test_should_build_rule_with_multiple_levels_of_redirect(self):
        # GIVEN
        rules = {
            0: [[1, 2]],
            1: [[3]],
            2: [[4]],
            3: [[5]],
            4: [[6]],
            5: "a",
            6: "b",
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("a").add_child(Node("b"))
            )
        )

    def test_should_manage_or(self):
        # GIVEN
        rules = {
            0: [[1, 2], [2, 1]],
            1: "a",
            2: "b"
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("a").add_child(Node("b")),
                Node("b").add_child(Node("a"))
            )
        )

    def test_should_build_or_at_nth_level(self):
        # GIVEN
        # accept bba or bab
        rules = {
            0: [[2, 1]],
            1: [[2, 3], [3, 2]],
            2: "b",
            3: "a",
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("b").add_children([
                    Node("b").add_child(Node("a")),
                    Node("a").add_child(Node("b")),
                ])
            )
        )

    def test_should_create_same_letter_tree(self):
        # GIVEN
        rules = {
            0: [[1, 2]],
            1: [[2, 2]],
            2: "a"
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_exactly(
                Node("a").add_child(Node("a")).add_child(Node("a"))
            )
        )

    def test_should_build_sub_second_example(self):
        # GIVEN
        #
        # a a a b
        #     b a
        # b b a b
        #     b a
        rules = {
            0: [[2, 3]],
            1: [[2, 3], [3, 2]],
            2: [[4, 4], [5, 5]],
            3: [[4, 5], [5, 4]],
            4: "a",
            5: "b"
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_inanyorder(
                Node("a").add_child(
                    Node("a").add_children([
                        Node("a").add_child(Node("b")),
                        Node("b").add_child(Node("a"))
                    ])
                ),
                Node("b").add_child(
                    Node("b").add_children([
                        Node("a").add_child(Node("b")),
                        Node("b").add_child(Node("a"))
                    ])
                )
            )
        )

    def test_should_link_to_end_of_branches(self):
        # GIVEN
        #
        # a b b a
        #
        rules = {
            0: [[1, 2]],
            1: [[3, 4]],
            2: [[4, 3]],
            3: "a",
            4: "b"
        }

        # WHEN
        nodes = _build_nodes(0, rules)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            nodes,
            contains_inanyorder(
                Node("a").add_child(
                    Node("b").add_child(
                        Node("b").add_child(
                            Node("a")
                        )
                    )
                )
            )
        )


class TestAddChildren:
    def test_should_not_overflow(self):
        # GIVEN
        node = Node("a").add_children([
            Node("a"),
            Node("b")
        ])

        # WHEN
        # the description of the behavior, is what will happen if we
        # think we are editing a tree, but we aren't we are editing a graph,
        # as some nodes might be shared by several branches

        # first add the same node to both branch
        node1 = Node("b")
        node.add_child(node1)

        # then add a new node to both branch, as both branch are already sharing
        # the same node, the first branch will add node2 to node1, then we will add
        # node2 to node2 as the second branch ahs already been updated because it share
        # the reference of node1
        node2 = Node("b")
        node.add_child(node2)

        # finally node3 is added, but if node2 already reference node2, we have a loop...
        # so we will just do a stack overflow...
        node3 = Node("a")
        node.add_child(node3)

        # THEN
        assert_that(
            node,
            equal_to(
                Node("a").add_children([
                    Node("a").add_child(Node("b")).add_child(Node("b")).add_child(Node("a")),
                    Node("b").add_child(Node("b")).add_child(Node("b")).add_child(Node("a"))
                ])
            )
        )
