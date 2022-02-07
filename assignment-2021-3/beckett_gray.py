import itertools
import sys

if sys.argv[-1] == "-r":
    numberOfBits = int(sys.argv[-2]) + 1
else:
    numberOfBits = int(sys.argv[-1]) + 1

def Delta(g):
    d = ""
    for m in range(len(g) - 1):
        d = d + str(len(str(abs(int(g[m])-int(g[m+1])))) - 1)
    return d


def Flip(x, b):
    return x ^ (1 << b)


def NumberToBin(codes, n):
    bins = []
    for c in codes:
        listOfBins = []
        for j in c:
            listOfBins.append(bin(j)[2:].zfill(n))
        bins.append(listOfBins)
    return bins


def changeToDelta(bits):
    dList = []
    for j in range(len(bits)):
        dList.append(Delta(bits[j]))
    return dList


visited = []
for k in range(2**numberOfBits):
    visited.append(False)

gc = [0]
all_codes = []
visited[0] = True


def GC(d, x, max_coord, n, gc):
    if d == 2**(n - 1):
        all_codes.append(gc.copy())
        return
    for y in range(0, min(n - 1, max_coord + 1)):
        x = Flip(x, y)
        if not visited[x]:
            visited[x] = True
            gc.append(x)
            GC(d + 1, x, max(y + 1, max_coord), n, gc)
            visited[x] = False
            gc.pop()
        x = Flip(x, y)


tail = []
def GC_BeckettGray(d, x, max_coord, n, gc, tail_in):
    if d == 2**(n-1):
        all_codes.append(gc.copy())
        return
    for y in range(0, min(n - 1, max_coord + 1)):
        x = Flip(x, y)
        if bin(x)[2:].zfill(n - 1)[-(y + 1)] == "0":
            if tail_in and y != tail_in[0]:
                x = Flip(x, y)
                continue
        if not visited[x]:
            visited[x] = True
            gc.append(x)
            last_changes = tail_in.copy()
            if bin(x)[2:].zfill(n - 1)[-(y + 1)] == "0":
                if y in tail_in:
                    tail_in.remove(y)
            else:
                if y in tail_in:
                    tail_in.remove(y)
                tail_in.append(y)
            GC_BeckettGray(d + 1, x, max(y + 1, max_coord), n, gc, tail_in)
            visited[x] = False
            gc.pop()
            tail_in = last_changes.copy()
        x = Flip(x, y)


def printAll(n, f, m):
    GC(1, 0, 0, numberOfBits, gc)
    circlesAndPaths = []
    for x in range(len(all_codes)):
        if bin(all_codes[x][-1]).count("1") == 1:
            all_codes[x].append(0)
            circlesAndPaths.append("C")
        else:
            circlesAndPaths.append("P")
    listWithBits = NumberToBin(all_codes, numberOfBits - 1)
    deltaList = changeToDelta(listWithBits)
    for i in range(len(deltaList)):
        print(circlesAndPaths[i], deltaList[i])
        if listWithBits[i][-1].count("1") == 0:
            listWithBits[i] = listWithBits[i][:-1].copy()
        if f:
            print(circlesAndPaths[i], *listWithBits[i])
        if m:
            table = []
            for num in range(n - 1):
                row = []
                for t in listWithBits[i]:
                    row.append(t[-(num + 1)])
                table.append(row)
            for t in table:
                print(*t)


def printCirclesBeckettGray(n, f, m):
    GC_BeckettGray(1, 0, 0, numberOfBits, gc, tail)
    deleteCodes = []
    for x in range(len(all_codes)):
        if bin(all_codes[x][-1]).count("1") == 1:
            all_codes[x].append(0)
        else:
            deleteCodes.append(all_codes[x])
    for i in deleteCodes:
        all_codes.remove(i)
    listWithBits = NumberToBin(all_codes, numberOfBits - 1)
    deltaList = changeToDelta(listWithBits)
    for i in range(len(deltaList)):
        print("B", deltaList[i])
        if f:
            print("B", *listWithBits[i][:-1])
        if m:
            table = []
            for num in range(n - 1):
                row = []
                for t in listWithBits[i][:-1]:
                    row.append(t[-(num + 1)])
                table.append(row)
            for t in table:
                print(*t)


def printBeckettGray(n, f, m):
    GC_BeckettGray(1, 0, 0, numberOfBits, gc, tail)
    for x in range(len(all_codes)):
        if bin(all_codes[x][-1]).count("1") == 1:
            all_codes[x].append(0)
    listWithBits = NumberToBin(all_codes, numberOfBits - 1)
    deltaList = changeToDelta(listWithBits)
    for i in range(len(deltaList)):
        print("U", deltaList[i])
        if listWithBits[i][-1].count("1") == 0:
            listWithBits[i] = listWithBits[i][:-1].copy()
        if f:
            print("U", *listWithBits[i])
        if m:
            table = []
            for num in range(n - 1):
                row = []
                for t in listWithBits[i]:
                    row.append(t[-(num + 1)])
                table.append(row)
            for t in table:
                print(*t)


def printCirclesOrPaths(c_p, n, f, m):
    GC(1, 0, 0, numberOfBits, gc)
    circlesAndPaths = []
    for x in range(len(all_codes)):
        if bin(all_codes[x][-1]).count("1") == 1:
            all_codes[x].append(0)
            circlesAndPaths.append("C")
        else:
            circlesAndPaths.append("P")
    listWithBits = NumberToBin(all_codes, numberOfBits - 1)
    deltaList = changeToDelta(listWithBits)
    for i in range(len(deltaList)):
        if listWithBits[i][-1].count("1") == 0:
            listWithBits[i] = listWithBits[i][:-1].copy()
        if circlesAndPaths[i] == c_p:
            print(circlesAndPaths[i], deltaList[i])
            if f:
                print(circlesAndPaths[i], *listWithBits[i])
            if m:
                table = []
                for num in range(n - 1):
                    row = []
                    for t in listWithBits[i]:
                        row.append(t[-(num + 1)])
                    table.append(row)
                for t in table:
                    print(*t)


def Isomorphic(bits):
    per_string = ""
    for x in range(0, bits - 1):
        per_string += str(x)
    listWithBits = NumberToBin(all_codes, numberOfBits - 1)
    deltaList = changeToDelta(listWithBits)
    permutations = itertools.permutations(per_string)
    isomorphic = {}
    for p in permutations:
        for y in range(len(deltaList)):
            list2 = ""
            for j in deltaList[y]:
                list2 += (p[int(j)])
            for c in range(y + 1, len(deltaList)):
                if deltaList[c][::-1] == list2:
                    isomorphic[len(isomorphic)+1] = deltaList[y], deltaList[c]
    isomorphic = sorted(isomorphic.values())
    for x in isomorphic:
        print(x[0], "<=>", x[1])


argvList = []
for a in sys.argv:
    argvList.append(a)

if "-a" in argvList or (("-r" in argvList and not argvList[1:-2]) or not argvList[1:-1]):
    if "-f" in argvList:
        if "-m" in argvList:
            printAll(numberOfBits, True, True)
        else:
            printAll(numberOfBits, True, False)
    elif "-m" in argvList:
        printAll(numberOfBits, False, True)
    else:
        printAll(numberOfBits, False, False)
elif "-b" in argvList:
    if "-f" in argvList:
        if "-m" in argvList:
            printCirclesBeckettGray(numberOfBits, True, True)
        else:
            printCirclesBeckettGray(numberOfBits, True, False)
    elif "-m" in argvList:
        printCirclesBeckettGray(numberOfBits, False, True)
    else:
        printCirclesBeckettGray(numberOfBits, False, False)
elif "-u" in argvList:
    if "-f" in argvList:
        if "-m" in argvList:
            printBeckettGray(numberOfBits, True, True)
        else:
            printBeckettGray(numberOfBits, True, False)
    elif "-m" in argvList:
        printBeckettGray(numberOfBits, False, True)
    else:
        printBeckettGray(numberOfBits, False, False)
elif "-c" in argvList:
    if "-f" in argvList:
        if "-m" in argvList:
            printCirclesOrPaths("C", numberOfBits, True, True)
        else:
            printCirclesOrPaths("C", numberOfBits, True, False)
    elif "-m" in argvList:
        printCirclesOrPaths("C", numberOfBits, False,  True)
    else:
        printCirclesOrPaths("C", numberOfBits, False, False)
elif "-p" in argvList:
    if "-f" in argvList:
        if "-m" in argvList:
            printCirclesOrPaths("P", numberOfBits, True, True)
        else:
            printCirclesOrPaths("P", numberOfBits, True, False)
    elif "-m" in argvList:
        printCirclesOrPaths("P", numberOfBits, False,  True)
    else:
        printCirclesOrPaths("P", numberOfBits, False, False)


if "-r" in argvList:
    Isomorphic(numberOfBits)
