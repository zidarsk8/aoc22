import util
from icecream import ic


text = """30373
25512
65332
33549
35390"""
# text = util.read_data(8)


trees = list(map(list, text.splitlines()))

visible = list(map(list, text.splitlines()))
distance = list(map(list, text.splitlines()))


for i in range(len(visible)):
    for j in range(len(visible[0])):
        visible[i][j] = 0

for i in range(len(visible)):
    visible[i][0] = 1
    visible[i][-1] = 1

for j in range(len(visible[0])):
    visible[0][j] = 1
    visible[-1][j] = 1

for i in range(len(visible)):
    for j in range(len(visible[0])):
        distance[i][j] = 1

for i in range(len(visible)):
    distance[i][0] = 0
    distance[i][-1] = 0

for j in range(len(visible[0])):
    distance[0][j] = 0
    distance[-1][j] = 0


ic("---------------")

for i, line in enumerate(trees):
    m = line[0]
    for j in range(1, len(line)):
        m = max(m, line[j - 1])
        if m < line[j]:
            visible[i][j] = 1


distance_map = {i: 1 for i in range(10)}

for i, line in enumerate(trees):
    m = line[0]
    distance_map[m] = 1
    for j in range(1, len(line)):
        visible_line = min(v for k, v in distance_map.items() if k >= line[j])
        distance[i][j] *= visible_line

        distance_map = {k: v + 1 for k, v in distance_map.items()}
        distance_map[line[j]] = 1

ic(trees)
ic(distance)
ic("---------------")

trees = [line[::-1] for line in trees]
visible = [line[::-1] for line in visible]


for i, line in enumerate(trees):
    m = line[0]
    for j in range(1, len(line)):
        m = max(m, line[j - 1])
        if m < line[j]:
            visible[i][j] = 1
        m = max(m, line[j - 1])

ic(trees)
ic(distance)
ic("---------------")


trees = list(map(list, zip(*trees[::-1])))
visible = list(map(list, zip(*visible[::-1])))


for i, line in enumerate(trees):
    m = line[0]
    for j in range(1, len(line)):
        m = max(m, line[j - 1])
        if m < line[j]:
            visible[i][j] = 1
        m = max(m, line[j - 1])


ic(trees)
ic(distance)
ic("---------------")

trees = [line[::-1] for line in trees]
visible = [line[::-1] for line in visible]


for i, line in enumerate(trees):
    m = line[0]
    for j in range(1, len(line)):
        m = max(m, line[j - 1])
        if m < line[j]:
            visible[i][j] = 1
        m = max(m, line[j - 1])


ic(trees)
ic(distance)
ic("---------------")

ic(sum(map(sum, visible)))
