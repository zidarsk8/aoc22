import pytest

import util

FULL_TEXT = util.read_data(9)


def get_code(text):
    return int(text)


@pytest.mark.parametrize(
    "text,result",
    [
        ("3", 3),
        ("13", 13),
    ],
)
def test_result(text, result):
    assert get_code(text) == result


def test_dummy():
    assert get_code("135") == 135


def draw_grid(grid):
    x_axis = [k[0] for k in grid]
    y_axis = [k[1] for k in grid]

    lines = [
        "".join(grid.get((x, y), ".") for x in range(min(x_axis), max(x_axis) + 1))
        for y in range(min(y_axis), max(y_axis) + 1)
    ]
    return lines[::-1]


@pytest.mark.parametrize(
    "grid,result",
    [
        ({(1, 3): "#"}, ["#"]),
        (
            {
                (1, 1): "#",
                (2, 2): "#",
            },
            [".#", "#."],
        ),
        (
            {
                (1, 1): "#",
                (5, 2): "#",
            },
            [
                "....#",
                "#....",
            ],
        ),
    ],
)
def test_draw_grid(grid, result):
    assert draw_grid(grid) == result


move = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def walk_head(steps):
    pos = (0, 0)
    grid = {pos: "H"}
    for direction, count in steps:
        for _ in range(count):
            pos = (pos[0] + move[direction][0], pos[1] + move[direction][1])
            grid[pos] = "H"
    return grid


@pytest.mark.parametrize(
    "moves,result",
    [
        ([("R", 4)], ["HHHHH"]),
        (
            [
                ("R", 4),
                ("U", 4),
            ],
            [
                "....H",
                "....H",
                "....H",
                "....H",
                "HHHHH",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
                ("L", 2),
                ("D", 2),
            ],
            [
                "..HHH",
                "..H.H",
                "..H.H",
                "....H",
                "HHHHH",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
                ("D", 2),
                ("L", 2),
            ],
            [
                "....H",
                "....H",
                "..HHH",
                "....H",
                "HHHHH",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
                ("D", 2),
                ("L", 2),
                ("D", 2),
            ],
            [
                "....H",
                "....H",
                "..HHH",
                "..H.H",
                "HHHHH",
            ],
        ),
    ],
)
def test_walk_head(moves, result):
    assert draw_grid(walk_head(moves)) == result


def move_tail(t_pos, h_pos):
    if abs(t_pos[0] - h_pos[0]) == 2 and abs(t_pos[1] - h_pos[1]) == 1:
        t_pos = (t_pos[0] + (h_pos[0] - t_pos[0]) // abs(h_pos[0] - t_pos[0]), h_pos[1])
    elif abs(t_pos[0] - h_pos[0]) == 1 and abs(t_pos[1] - h_pos[1]) == 2:
        t_pos = (h_pos[0], t_pos[1] + (h_pos[1] - t_pos[1]) // abs(h_pos[1] - t_pos[1]))
    elif abs(t_pos[0] - h_pos[0]) > 1:
        t_pos = (t_pos[0] + (h_pos[0] - t_pos[0]) // abs(h_pos[0] - t_pos[0]), t_pos[1])
    elif abs(t_pos[1] - h_pos[1]) > 1:
        t_pos = (t_pos[0], t_pos[1] + (h_pos[1] - t_pos[1]) // abs(h_pos[1] - t_pos[1]))
    return t_pos


@pytest.mark.parametrize(
    "t_pos,h_pos,result",
    [
        # x lateral
        ((1, 1), (1, 1), (1, 1)),
        ((1, 1), (1, 2), (1, 1)),
        ((1, 1), (2, 1), (1, 1)),
        ((1, 1), (2, 2), (1, 1)),
        ((1, 1), (0, 2), (1, 1)),
        ((1, 1), (3, 1), (2, 1)),
        ((3, 1), (5, 1), (4, 1)),
        ((3, 3), (5, 3), (4, 3)),
        ((-3, 3), (-5, 3), (-4, 3)),
        # y lateral
        ((1, 3), (1, 5), (1, 4)),
        ((1, -3), (1, -5), (1, -4)),
        # side
        ((1, 3), (2, 5), (2, 4)),
    ],
)
def test_move_tail(t_pos, h_pos, result):
    assert move_tail(t_pos, h_pos) == result


move = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def walk_tail(steps):
    h_pos = (0, 0)
    t_pos = (0, 0)
    grid = {t_pos: "T"}
    for direction, count in steps:
        for _ in range(count):
            h_pos = (h_pos[0] + move[direction][0], h_pos[1] + move[direction][1])
            t_pos = move_tail(t_pos, h_pos)
            grid[t_pos] = "T"
    return grid


@pytest.mark.parametrize(
    "moves,result",
    [
        ([("R", 1)], ["T"]),
        ([("R", 2)], ["TT"]),
        ([("R", 3)], ["TTT"]),
        ([("R", 4)], ["TTTT"]),
        (
            [
                ("R", 4),
                ("U", 4),
            ],
            [
                "....T",
                "....T",
                "....T",
                "TTTT.",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
                ("D", 1),
                ("R", 1),
            ],
            [
                "....T",
                "....T",
                "....T",
                "TTTT.",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
                ("D", 1),
                ("R", 1),
                ("R", 1),
            ],
            [
                "....TT",
                "....T.",
                "....T.",
                "TTTT..",
            ],
        ),
        (
            [
                ("R", 4),
                ("U", 4),
            ],
            [
                "....T",
                "....T",
                "....T",
                "TTTT.",
            ],
        ),
        (
            [
                ("R", 4),
                ("D", 2),
            ],
            [
                "TTTT.",
                "....T",
            ],
        ),
        (
            [
                ("R", 4),
                ("D", 1),
                ("R", 1),
            ],
            [
                "TTTT.",
                "....T",
            ],
        ),
    ],
)
def test_walk_tail(moves, result):
    assert draw_grid(walk_tail(moves)) == result


def part_1(input_text):
    moves = [[m.split()[0], int(m.split()[1])] for m in input_text.splitlines()]
    tail_grid = walk_tail(moves)
    return len(tail_grid)


example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


@pytest.mark.parametrize(
    "input_text,result",
    [
        (example, 13),
        (FULL_TEXT, 5878),
    ],
)
def test_part_(input_text, result):
    assert part_1(input_text) == result
