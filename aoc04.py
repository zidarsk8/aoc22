import util

text = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
# print(text)
text = util.read_data(4)
lines = text.splitlines()


cnt = 0
for line in lines:
    e1, e2 = line.split(",")
    r1 = set(range(int(e1.split("-")[0]), int(e1.split("-")[1]) + 1))
    r2 = set(range(int(e2.split("-")[0]), int(e2.split("-")[1]) + 1))
    print(r1, r2)
    # if r1 <= r2 or r2 <= r1:
    if r1 & r2:
        cnt += 1
print(cnt)


# print(lines)
