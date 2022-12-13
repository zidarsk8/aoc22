import pytest
from textwrap import dedent

import util

input_text = util.read_data(13)


short_example = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()


from icecream import ic


def parse_pairs(input_text: str) -> list[tuple[list, list]]:
    pairs = input_text.split("\n\n")
    result = []
    for pair in pairs:
        first, second = pair.splitlines()
        result.append((eval(first), eval(second)))

    return result


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                [7,7,7,7]
                [7,7,7]
                """
            ).strip(),
            [
                (
                    [7, 7, 7, 7],
                    [7, 7, 7],
                )
            ],
        ),
        (
            dedent(
                """
                [7,7,7,7]
                [7,7,7]

                []
                [3]

                [[[]]]
                [[]]
                """
            ).strip(),
            [
                (
                    [7, 7, 7, 7],
                    [7, 7, 7],
                ),
                (
                    [],
                    [3],
                ),
                (
                    [[[]]],
                    [[]],
                ),
            ],
        ),
    ],
)
def test_parse_pairs(text: str, result):
    assert parse_pairs(text) == result


def compare(first, second) -> bool:
    f, s = make_same(first, second)
    return f <= s


def make_same(first, second):
    if len(first) > len(second):
        first_part, second_part = make_same(first[: len(second)], second)
        return first_part + first[len(second) :], second_part

    if len(first) < len(second):
        first_part, second_part = make_same(first, second[: len(first)])
        return first_part, second_part + second[len(first) :]

    first = [
        [f] if isinstance(f, int) and isinstance(s, list) else f
        for f, s in zip(first, second)
    ]
    second = [
        [s] if isinstance(s, int) and isinstance(f, list) else s
        for f, s in zip(first, second)
    ]

    first = [
        make_same(f, s)[0] if isinstance(f, list) else f for f, s in zip(first, second)
    ]

    second = [
        make_same(f, s)[1] if isinstance(f, list) else s for f, s in zip(first, second)
    ]

    return first, second


@pytest.mark.parametrize(
    "pairs,result",
    [
        (
            (
                [1, 2, 3, 5],
                [4, 9],
            ),
            (
                [1, 2, 3, 5],
                [4, 9],
            ),
        ),
        (
            (
                [4, 9],
                [1, [2], 3, 5],
            ),
            (
                [4, [9]],
                [1, [2], 3, 5],
            ),
        ),
        (
            (
                [4, 9],
                [1, 2, 31, [5]],
            ),
            (
                [4, 9],
                [1, 2, 31, [5]],
            ),
        ),
        (
            (
                [1],
                [],
            ),
            (
                [1],
                [],
            ),
        ),
        (
            (
                [1, 2, 5],
                [[5], 1, [16]],
            ),
            (
                [[1], 2, [5]],
                [[5], 1, [16]],
            ),
        ),
        (
            (
                [1, 2, 5],
                [[[5]], 1, 16],
            ),
            (
                [[[1]], 2, 5],
                [[[5]], 1, 16],
            ),
        ),
        (
            (
                [1, 2, [5, [5]]],
                [[[]], 1, 16],
            ),
            (
                [[[1]], 2, [5, [5]]],
                [[[]], 1, [16]],
            ),
        ),
    ],
)
def test_make_same(pairs, result):
    assert make_same(pairs[0], pairs[1]) == result


@pytest.mark.parametrize(
    "pairs,result",
    [
        (
            (
                [1, 1, 3, 1, 1],
                [1, 1, 5, 1, 1],
            ),
            True,
        ),
        (
            (
                [[1], [2, 3, 4]],
                [[1], 4],
            ),
            True,
        ),
        (
            (
                [9],
                [[8, 7, 6]],
            ),
            False,
        ),
        (
            (
                [[4, 4], 4, 4],
                [[4, 4], 4, 4, 4],
            ),
            True,
        ),
        (
            (
                [7, 7, 7, 7],
                [7, 7, 7],
            ),
            False,
        ),
        (
            (
                [],
                [3],
            ),
            True,
        ),
        (
            (
                [[[]]],
                [[]],
            ),
            False,
        ),
        (
            (
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
            ),
            False,
        ),
    ],
)
def test_compare(pairs, result):
    first, second = make_same(pairs[0], pairs[1])

    assert compare(first, second) == result


def correct_pairs(text):
    pairs = parse_pairs(text)
    good_indexes = [i + 1 for i, pair in enumerate(pairs) if compare(pair[0], pair[1])]
    return sum(good_indexes)


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                [7,7,7,7]
                [7,7,7]
                """
            ).strip(),
            0,
        ),
        (
            dedent(
                """
                [7,7,7,7]
                [7,7,7]

                []
                [3]

                [[[]]]
                [[]]
                """
            ).strip(),
            2,
        ),
        (
            short_example,
            13,
        ),
        (
            input_text,
            4894,
        ),
    ],
)
def test_correct_pairs(text: str, result):
    assert correct_pairs(text) == result


def part2(text):
    pairs = parse_pairs(text)
    flat = sum(map(list, pairs), [])
    ic(flat)
    pos2 = sum([1 for item in flat if not compare([[2]], item)]) + 1
    pos6 = sum([1 for item in flat if not compare([[6]], item)]) + 2
    ic(pos2)
    ic(pos6)
    return pos2 * pos6


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                [7,7,7,7]
                [5,7,7]
                """
            ).strip(),
            3,
        ),
        (
            dedent(
                """
                 [7,7,7,7]
                 [7,7,7]
                 
                 []
                 [3]

                 [[[]]]
                 [[]]
                 """
            ).strip(),
            24,
        ),
        (
            short_example,
            140,
        ),
        (
            input_text,
            24180,
        ),
    ],
)
def test_part2(text: str, result):
    assert part2(text) == result
