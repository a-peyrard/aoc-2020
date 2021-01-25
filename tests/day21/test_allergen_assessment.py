from hamcrest import assert_that, contains_inanyorder

from aoc.day21.allergen_assessment import _parse, Food


class TestParse:
    def test_should_parse_given_foods(self):
        # GIVEN
        raw = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

        # WHEN
        foods = _parse(raw.splitlines(keepends=True))

        # THEN
        assert_that(
            foods,
            contains_inanyorder(
                Food(
                    ingredients={"mxmxvkd", "kfcds", "sqjhc", "nhms"},
                    allergens={"dairy", "fish"},
                ),
                Food(
                    ingredients={"trh", "fvjkl", "sbzzf", "mxmxvkd"},
                    allergens={"dairy"},
                ),
                Food(
                    ingredients={"sqjhc", "fvjkl"},
                    allergens={"soy"},
                ),
                Food(
                    ingredients={"sqjhc", "mxmxvkd", "sbzzf"},
                    allergens={"fish"},
                )
            )
        )
