import util

text = util.read_data(3)
# print(text)
lines = text.splitlines()


def chr_to_val(c):
    if c > "Z":
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27


common = []
for line in lines:
    first, second = line[: len(line) // 2], line[len(line) // 2 :]
    common.append(chr_to_val((set(first) & set(second)).pop()))

print(sum(common))


common = []
for i in range(0, len(lines), 3):
    group = list(map(set, lines[i : i + 3]))
    c = group[0] & group[1] & group[2]
    common.append(chr_to_val(c.pop()))

print(sum(common))
