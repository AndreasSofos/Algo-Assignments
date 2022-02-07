import itertools
import sys

file = open(sys.argv[-1], "r")
lines = file.read().splitlines()


points = []
for line in lines:
    points.append(line.split(" "))

maxCol = 0
maxRow = 0
for i in points:
    if int(i[0]) > maxCol:
        maxCol = int(i[0])
    if int(i[1]) > maxRow:
        maxRow = int(i[1])


for i in range(len(points)):
    points[i] = ([int(points[i][0]), int(points[i][1])])
points.sort()

lines = {}
for i in range(1, maxCol + 1):
    col = []
    for j in points:
        if int(j[0]) == i:
            col.append(j)
    if len(col) > 1:
        col.sort()
        lines[len(lines) + 1] = col

for i in range(1, maxRow + 1):
    row = []
    for j in points:
        if int(j[1]) == i:
            row.append(j)
    row.sort()
    if len(row) == 1:
        row.append([row[0][0] + 1, row[0][1]])
    lines[len(lines) + 1] = row


def diagonals(points):
    old_points = list(points)
    for n in range(len(points)):
        points = list(old_points)
        k = n + 1
        while k < len(points):
            diag = [points[n]]
            if int(points[k][0]) != int(diag[0][0]) and int(points[k][1]) != int(diag[0][1]):
                diag.append(points[k])
                for p in points:
                    if int(p[0]) - int(diag[-1][0]) == int(diag[-1][0]) - int(diag[-2][0]) and int(p[1]) - int(diag[-1][1]) == int(diag[-1][1]) - int(diag[-2][1]):
                        diag.append(p)
                if len(diag) >= 2:
                    for d in diag:
                        if d != points[n]:
                            points.remove(d)
                    lines[len(lines) + 1] = diag
                    k = n
            k += 1
    points = list(old_points)
    return lines, points

def regular():
    sol = []
    flag = True
    i = 2
    while flag:
        p = itertools.combinations(lines, i)
        for j in list(p):
            universe = []
            for line in j:
                for point in lines[line]:
                    if point not in universe and point in points:
                        universe.append(point)
            universe.sort()
            if universe == points:
                sol = j
                flag = False
                break
        i += 1
    return sol


def Diff(li1, li2):
    li_dif = [j for j in li2 if j not in li1 or j not in li2]
    return li_dif

def greedy(points):
    sol = []
    flag1 = True
    while flag1:
        dif_len = len(points)
        line = 1
        for i in range(1, len(lines) + 1):
            diff = Diff(lines[i], points)
            if len(diff) < dif_len:
                dif_len = len(diff)
                line = i
        if line not in sol:
            points = Diff(lines[line], points)
            sol.append(line)
        if len(points) == 0:
            flag1 = False
    return sol


if sys.argv[-2] != "-g":
    lines, points = diagonals(points)
if sys.argv[1] == "-f":
    sol = regular()
else:
    sol = greedy(points)


sol_list = []
for i in sol:
    sol_list.append(lines[i])

sol_list.sort()
sol_list = sorted(sol_list, key=len, reverse=True)
for i in sol_list:
    for j in i:
        print(str(j).replace('[', '(').replace(']', ')'), end=" ")
    print(" ")
