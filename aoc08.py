import util
from icecream import ic


text = """30373
25512
65332
33549
35390"""
text = util.read_data(8)


trees = list(map(list, text.splitlines()))
trees = [list(map(int, line)) for line in trees]

distance = list(map(list, text.splitlines()))


for i in range(len(distance)):
    for j in range(len(distance[0])):
        distance[i][j] = 1

for i in range(len(distance)):
    distance[i][0] = 0
    distance[i][-1] = 0

for j in range(len(distance[0])):
    distance[0][j] = 0
    distance[-1][j] = 0


def left_distance(trees, distance):
    for i, line in enumerate(trees):
        distance_map = {i: 1 for i in range(10)}
        for j in range(1, len(line)):
            visible_line = min(v for k, v in distance_map.items() if k >= line[j])
            distance[i][j] *= visible_line

            distance_map = {k: v + 1 for k, v in distance_map.items()}
            distance_map[line[j]] = 1
    return distance


distance = left_distance(trees, distance)

ic("---------------")
trees = [line[::-1] for line in trees]
distance = [line[::-1] for line in distance]
distance = left_distance(trees, distance)

ic("---------------")
trees = list(map(list, zip(*trees[::-1])))
distance = list(map(list, zip(*distance[::-1])))
distance = left_distance(trees, distance)

ic("---------------")
trees = [line[::-1] for line in trees]
distance = [line[::-1] for line in distance]
distance = left_distance(trees, distance)


ic("---------------")
trees = list(map(list, zip(*trees[::-1])))
distance = list(map(list, zip(*distance[::-1])))

ic("---------------")

ic(max(map(max, distance)))
