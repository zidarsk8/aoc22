import util

text = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
# print(text)
text = util.read_data(5)

crates = list(map(list, text.split("\n\n")[0].splitlines()))
crates = [[i for i in c if i != " "] for c in zip(*crates[::-1]) if c[0] != " "]

moves = [line.split() for line in text.split("\n\n")[1].splitlines()]
moves = [[int(num), int(f) - 1, int(t) - 1] for _, num, _, f, _, t in moves]

# part 1
# for num, f, t in moves:
#     for _ in range(num):
#         crates[t].append(crates[f].pop())
#
# print("".join([c[-1] for c in crates]))

for num, f, t in moves:
    crates[t] += crates[f][-num:]
    crates[f] = crates[f][:-num]

print("".join([c[-1] for c in crates]))
