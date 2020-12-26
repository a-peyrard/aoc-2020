import re
from typing import Callable, List, Optional, Set

ValueValidator = Callable[[Optional[str]], bool]
ValueExtractor = Callable[[str], Optional[str]]


def number_validator(min_bound: int, max_bound: int) -> ValueValidator:
    def validator(val: str) -> bool:
        try:
            return min_bound <= int(val) <= max_bound
        except (ValueError, TypeError):
            return False

    return validator


def or_validator(validators: List[ValueValidator]) -> ValueValidator:
    return lambda val: any((validator(val) for validator in validators))


def exists_validator(val: Optional[str]) -> bool:
    return val is not None


def in_validator(allowed_values: Set[str]) -> ValueValidator:
    return lambda val: val in allowed_values


def regex_extractor(regex: str) -> ValueExtractor:
    pattern = re.compile(regex)

    def extractor(val: str) -> Optional[str]:
        matcher = pattern.search(val)
        if matcher and len(matcher.groups()) == 1:
            return matcher.group(1)

        return None

    return extractor