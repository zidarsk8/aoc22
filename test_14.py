from textwrap import dedent

import pytest

import util

input_text = util.read_data(13)

from icecream import ic

short_example = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

ic(short_example)


def parse_lines(text: str) -> list[list[list[int]]]:
    lines = []
    for line in text.splitlines():
        parts = [list(map(int, p.strip().split(","))) for p in line.split("->")]
        lines.extend(list(zip(parts[:-1], parts[1:])))

    return lines


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                498,4 -> 498,6
                """
            ).strip(),
            [([498, 4], [498, 6])],
        ),
        (
            dedent(
                """
                498,4 -> 498,6 -> 496,6
                """
            ).strip(),
            [
                ([498, 4], [498, 6]),
                ([498, 6], [496, 6]),
            ],
        ),
        (
            dedent(
                """
                498,4 -> 498,6 -> 496,6
                503,4 -> 502,4 -> 502,9 -> 494,9
                """
            ).strip(),
            [
                ([498, 4], [498, 6]),
                ([498, 6], [496, 6]),
                ([503, 4], [502, 4]),
                ([502, 4], [502, 9]),
                ([502, 9], [494, 9]),
            ],
        ),
    ],
)
def test_parse_pairs(text: str, result):
    assert parse_lines(text) == result


def draw_grid(grid):
    x = [k[0] for k in grid]
    y = [k[1] for k in grid]
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    ic(min_x)

    return "\n".join(
        [
            "".join([grid.get((x, y), ".") for x in range(min_x - 3, max_x + 4)])
            for y in range(-1, max_y + 3)
        ]
    )


@pytest.mark.parametrize(
    "grid,result",
    [
        (
            {(499, 2): "#"},
            dedent(
                """
                .......
                .......
                .......
                ...#...
                .......
                .......
                """
            ).strip(),
        ),
        (
            {
                (499, 2): "#",
                (499, 3): "#",
                (499, 4): "#",
                (500, 4): "#",
            },
            dedent(
                """
                ........
                ........
                ........
                ...#....
                ...#....
                ...##...
                ........
                ........
                """
            ).strip(),
        ),
        (
            {
                (500, 0): "+",
                (499, 2): "#",
                (499, 3): "#",
                (499, 4): "#",
                (500, 4): "#",
            },
            dedent(
                """
                ........
                ....+...
                ........
                ...#....
                ...#....
                ...##...
                ........
                ........
                """
            ).strip(),
        ),
    ],
)
def test_draw_grid(grid: str, result):
    assert draw_grid(grid) == result


def fill_grid(lines):
    grid = {}
    for p1, p2 in lines:
        for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])):
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])):
                grid[(x, y)] = "#"
    return grid


@pytest.mark.parametrize(
    "grid,result",
    [
        (
            [([498, 4], [498, 6])],
            {
                (498, 4): "#",
                (498, 5): "#",
                (498, 6): "#",
            },
        ),
        # (
        #     [
        #         ([498, 4], [498, 6]),
        #         ([498, 6], [496, 6]),
        #     ],
        #     {
        #         (498, 4): "#",
        #         (498, 5): "#",
        #         (498, 6): "#",
        #         (497, 6): "#",
        #         (496, 6): "#",
        #     },
        # ),
        # (
        #     [
        #         ([498, 4], [498, 6]),
        #         ([498, 6], [496, 6]),
        #         ([503, 4], [502, 4]),
        #         ([502, 4], [502, 9]),
        #         ([502, 9], [494, 9]),
        #     ],
        #     {
        #         # line 1
        #         (498, 4): "#",
        #         (498, 5): "#",
        #         (498, 6): "#",
        #         # line 2
        #         (497, 6): "#",
        #         (496, 6): "#",
        #         # line 3
        #         (503, 4): "#",
        #         (502, 4): "#",
        #         # line 4
        #         (502, 4): "#",
        #         (502, 5): "#",
        #         (502, 6): "#",
        #         (502, 7): "#",
        #         (502, 8): "#",
        #         (502, 9): "#",
        #         # line 5
        #         (502, 9): "#",
        #         (501, 9): "#",
        #         (500, 9): "#",
        #         (499, 9): "#",
        #         (498, 9): "#",
        #         (497, 9): "#",
        #         (496, 9): "#",
        #         (495, 9): "#",
        #         (494, 9): "#",
        #     },
        # ),
    ],
)
def test_draw_grid(grid: str, result):
    assert draw_grid(grid) == result
