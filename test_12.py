import pytest
from textwrap import dedent

import util

input_text = util.read_data(12)


short_example = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()


from icecream import ic

Grid = list[list[str]]
Point = tuple[int, int]


def parse_map(input_text: str) -> Grid:
    return [list(line) for line in input_text.splitlines()]


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                Sa
                ab
                """
            ).strip(),
            [
                ["S", "a"],
                ["a", "b"],
            ],
        ),
        (
            short_example,
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
        ),
    ],
)
def test_parse_map(text: str, result: Grid):
    assert parse_map(text) == result


def find_position(grid: Grid, char: str) -> set[Point]:
    return {
        (x, y) for x, line in enumerate(grid) for y, c in enumerate(line) if c == char
    }


@pytest.mark.parametrize(
    "grid,char,result",
    [
        (
            [
                ["S", "a"],
                ["a", "b"],
            ],
            "S",
            {(0, 0)},
        ),
        (
            [
                ["S", "a"],
                ["a", "b"],
            ],
            "X",
            set(),
        ),
        (
            [
                ["S", "a", "e"],
                ["a", "b", "c"],
                ["a", "E", "c"],
                ["a", "b", "c"],
            ],
            "E",
            {(2, 1)},
        ),
        (
            [
                ["S", "a", "e"],
                ["a", "b", "c"],
                ["a", "E", "c"],
                ["a", "E", "E"],
            ],
            "E",
            {(2, 1), (3, 1), (3, 2)},
        ),
        (
            parse_map(input_text),
            "E",
            {(20, 77)},
        ),
        (
            parse_map(input_text),
            "S",
            {(20, 0)},
        ),
    ],
)
def test_find_position(grid, char, result):
    assert find_position(grid, char) == result


def is_legal_move(grid, pos, new_pos):
    if (
        new_pos[0] < 0
        or new_pos[1] < 0
        or new_pos[0] >= len(grid)
        or new_pos[1] >= len(grid[0])
    ):
        return False
    if grid[pos[0]][pos[1]] == "S":
        return True
    if grid[new_pos[0]][new_pos[1]] == "E":
        return grid[pos[0]][pos[1]] == "z"
    if ord(grid[new_pos[0]][new_pos[1]]) - ord(grid[pos[0]][pos[1]]) > 1:
        return False
    return True


def get_moves(grid: Grid, pos: Point) -> set[Point]:
    moves = set()
    for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if is_legal_move(grid, pos, new_pos):
            moves.add(new_pos)
    return moves


@pytest.mark.parametrize(
    "grid,pos,result",
    [
        (
            [
                ["S", "a"],
                ["a", "b"],
            ],
            (0, 0),
            {(1, 0), (0, 1)},
        ),
        (
            [
                ["S", "a", "e"],
                ["a", "b", "c"],
                ["a", "d", "c"],
                ["a", "b", "c"],
            ],
            (1, 1),
            {(1, 2), (1, 0), (0, 1)},
        ),
        (
            [
                ["S", "a", "e"],
                ["a", "b", "c"],
                ["a", "E", "c"],
                ["a", "b", "c"],
            ],
            (3, 1),
            {(3, 2), (3, 0)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            (1, 3),
            {(1, 2), (0, 3), (2, 3)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            (3, 7),
            {(4, 7), (2, 7)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            (2, 4),
            {(2, 5), (2, 3), (3, 4), (1, 4)},
        ),
    ],
)
def test_get_moves(grid, pos, result):
    assert get_moves(grid, pos) == result


def step(
    grid: Grid,
    current_positions: set[Point],
    visited: set[Point],
) -> tuple[set[Point], set[Point]]:
    new_positions = set()
    for pos in current_positions:
        for new_pos in get_moves(grid, pos) - visited:
            new_positions.add(new_pos)

    return new_positions, visited | new_positions


@pytest.mark.parametrize(
    "grid,current_positions,visited,expected_positions,expected_visited",
    [
        (
            [
                ["S", "a"],
                ["a", "b"],
            ],
            {(0, 0)},
            {(0, 0)},
            {(0, 1), (1, 0)},
            {(0, 0), (0, 1), (1, 0)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            {(0, 1), (1, 0)},
            {(0, 0), (0, 1), (1, 0)},
            {(0, 2), (1, 1), (2, 0)},
            {(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            {(0, 2), (1, 1), (2, 0)},
            {(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0)},
            {(1, 2), (2, 1), (3, 0)},
            {(1, 2), (2, 1), (3, 0), (0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0)},
        ),
        (
            [
                ["S", "a", "b", "q", "p", "o", "n", "m"],
                ["a", "b", "c", "r", "y", "x", "x", "l"],
                ["a", "c", "c", "s", "z", "E", "x", "k"],
                ["a", "c", "c", "t", "u", "v", "w", "j"],
                ["a", "b", "d", "e", "f", "g", "h", "i"],
            ],
            {(2, 4)},
            {(2, 4)},
            {(2, 5), (2, 3), (3, 4), (1, 4)},
            {(2, 4), (2, 5), (2, 3), (3, 4), (1, 4)},
        ),
    ],
)
def test_step(grid, current_positions, visited, expected_positions, expected_visited):
    new_positions, new_visited = step(grid, current_positions, visited)
    assert new_positions == expected_positions
    assert new_visited == expected_visited


def walk(text, start_char, end_char):
    grid = parse_map(text)
    start = find_position(grid, start_char)
    end = find_position(grid, end_char).pop()
    current_positions = start
    visited = start
    steps = 0
    while end not in visited and current_positions:
        current_positions, visited = step(grid, current_positions, visited)
        steps += 1
    return steps


@pytest.mark.parametrize(
    "text,start_char,end_char,steps",
    [
        (
            short_example,
            "S",
            "E",
            31,
        ),
        (
            input_text,  # part 1
            "S",
            "E",
            361,
        ),
        (
            input_text,  # part 2
            "a",
            "E",
            354,
        ),
    ],
)
def test_walk(text, start_char, end_char, steps):
    assert walk(text, start_char, end_char) == steps
