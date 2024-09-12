"""
Copyright (c) 2024 Grayson Boyer and Victor Ignatenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import re
from typing import Generator
from typing import Any


class ChemparseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ParenthesesMismatchError(ChemparseError):
    def __init__(self, formula: str) -> None:
        super().__init__(f"Open and closed parentheses mismatch in formula '{formula}'")


class NestedParenthesesError(ChemparseError):
    def __init__(self, formula: str) -> None:
        super().__init__(f"Cannot parse nested parentheses in formula '{formula}'")


class ClosedParenthesesBeforeOpenError(ChemparseError):
    def __init__(self, formula: str) -> None:
        super().__init__(f"Closed parentheses detected before open parentheses in formula '{formula}'")


RE_SIGNED_NUMBER: str = r"(^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)([eE][+-]?\d+)?)"
RE_NUMBER: str = r"(^(?=.)(([0-9]*)(\.([0-9]+))?)([eE][+-]?\d+)?)"
RE_LETTERS: str = r"^[a-zA-Z-+]+"


# function to return index of all instances of a substring in a string


def find_all(sub: str, a_str: str) -> Generator[int, Any, None]:
    start: int = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


# functions to parse elemental formulas (handles both floats and ints)
def get_first_elem(formula: str) -> tuple[str, bool]:
    needed_split: bool = False
    for char in formula:
        if formula.find(char) != 0 and (char.isupper() or char == "+" or char == "-"):
            formula = formula.split(char)[0]
            needed_split = True
            return formula, needed_split

        char_ind = list(find_all(char, formula))
        if len(char_ind) > 1 and (char.isupper() or char == "+" or char == "-") and (
                formula[1] == char or formula[1].islower()) and sum(
            1 for c in formula[0:char_ind[1]] if c.isupper()) == 1:
            formula = formula[0:char_ind[1]]
            needed_split = True
            return formula, needed_split

    return formula, needed_split


def inner_parse_formula(text: str) -> dict[str, float]:
    formula_dict: dict[str, float] = {}
    for _ in range(0, len(text)):
        element = re.findall(RE_LETTERS, text)
        if len(element) == 0:
            break
        else:
            element, needed_split = get_first_elem(element[0])
            text = text.replace(element, '', 1)
            if needed_split:
                number = 1.0
            else:
                try:
                    number = float(re.findall(RE_SIGNED_NUMBER, text)[0][0])
                except:
                    number = 1.0
                text = re.sub(RE_SIGNED_NUMBER, "", text)
            if element not in list(formula_dict.keys()):
                formula_dict[element] = number
            else:
                formula_dict[element] += number
    return formula_dict


def find_occurrences(s: str, ch: str) -> list[int]:
    return [i for i, letter in enumerate(s) if letter == ch]


def get_first_parenth_match(text: str) -> int:
    position: int = -1
    ch_number: int = 0
    closed_parenth_count: int = 0
    opened_parenth_count: int = 0
    for ch in text:
        if ch == '(':
            opened_parenth_count += 1
        elif ch == ')':
            closed_parenth_count += 1
            if opened_parenth_count == closed_parenth_count:
                position = closed_parenth_count - 1
                break
        ch_number += 1

    return position


def parse_formula(text: str) -> dict[str, float]:

    text = str(text)
    text = text.replace("[", "(")
    text = text.replace("]", ")")

    # get indices of starting parentheses "(" and ending ")"
    open_parenth_idx_list = find_occurrences(text, "(")
    closed_parenth_idx_list = find_occurrences(text, ")")

    if len(open_parenth_idx_list) != len(closed_parenth_idx_list):
        raise ParenthesesMismatchError(text)

    for i in range(0, len(open_parenth_idx_list) - 1):
        # if open_parenth_idx_list[i+1] < closed_parenth_idx_list[i]:
        #     raise NestedParenthesesError(text)
        if closed_parenth_idx_list[i] < open_parenth_idx_list[i]:
            raise ClosedParenthesesBeforeOpenError(text)
        if i == len(open_parenth_idx_list) - 1:
            if closed_parenth_idx_list[i + 1] < open_parenth_idx_list[i + 1]:
                raise ClosedParenthesesBeforeOpenError(text)

    seg_dict_list: list[dict[str, float]] = []
    parenth_pairs_count = len(open_parenth_idx_list)
    for _ in range(parenth_pairs_count):
        text = str(text)
        if len(text) <= 0:
            break
        if not '(' in text and not ')' in text:
            break

        # get indices of starting parentheses "(" and ending ")"
        open_parenth_idx_list = find_occurrences(text, "(")
        closed_parenth_idx_list = find_occurrences(text, ")")

        first_parenth_match: int = get_first_parenth_match(text)
        if first_parenth_match < 0:
            raise ParenthesesMismatchError(text)
        seg = text[open_parenth_idx_list[0]:closed_parenth_idx_list[first_parenth_match] + 1]

        try:
            number = float(re.findall(RE_SIGNED_NUMBER, text[closed_parenth_idx_list[first_parenth_match] + 1:])[0][0])
        except:
            number = 1

        seg_no_parenth = seg[1:-1]
        # nested_parenth:bool = False
        if '(' in seg_no_parenth or ')' in seg_no_parenth:
            seg_formula_dict = parse_formula(seg_no_parenth)
            # nested_parenth = True

        else:
            seg_formula_dict = inner_parse_formula(seg_no_parenth)
        seg_formula_dict_mult = {k: v * number for (k, v) in seg_formula_dict.items()}

        endseg = re.sub(RE_NUMBER, "", text[closed_parenth_idx_list[first_parenth_match] + 1:])
        # if not nested_parenth:
        text = text[:open_parenth_idx_list[0]] + endseg
        seg_dict_list.append(seg_formula_dict_mult)

    if '(' in text in text:
        seg_dict_list.append(parse_formula(text))
    else:
        seg_dict_list.append(inner_parse_formula(text))

    # merge and sum all segments
    if len(seg_dict_list) > 1:
        start_dict = seg_dict_list[0]
        for i in range(1, len(seg_dict_list)):
            next_dict = seg_dict_list[i]
            start_dict = {k: start_dict.get(k, 0) + next_dict.get(k, 0) for k in set(start_dict) | set(next_dict)}
        return start_dict
    else:
        return seg_dict_list[0]
