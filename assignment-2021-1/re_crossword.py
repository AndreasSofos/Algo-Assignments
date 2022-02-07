import re
import string
import sre_yield
import sys

f1 = open(sys.argv[2])
reg_exp = f1.read().splitlines()

words = {}
c1 = 0
for x in reg_exp:
    words[c1] = x
    c1 += 1

f2 = open(sys.argv[1])
crossword_structure = f2.read().splitlines()

crossword = list()
for x in crossword_structure:
    crossword.append(x)

crossword_dict = {}

for i in range(len(crossword)):
    crossword_dict[int(crossword[i].split(",", 1)[0])] = crossword[i].split(",", 2)[1], crossword[i].split(",", 2)[
        2], int(crossword[i].split(",", 2)[0])

cuts = []

for i in range(len(crossword_dict.keys())):
    cuts.append([-1 for j in range(len(crossword_dict.keys()))])
    for m in range(1, (len(crossword_dict[i][1]) + 1) // 4 + 1):
        crossed_word = int(crossword_dict[i][1].split(",")[m * 2 - 2])
        common_letter_pos = int(crossword_dict[i][1].split(",")[m * 2 - 1])
        cuts[i][crossed_word] = common_letter_pos


for i in crossword_dict.keys():
    for j in words.keys():
        if crossword_dict[i][0] == words[j]:
            crossword_dict[i] = crossword_dict[i][0], crossword_dict[i][1], words[j]
            del words[j]
            break

deleted_words = []
original_words = dict(words)
original_cross_dict = dict(crossword_dict)
last_min = []
keep_pos = []
counter = 0
matching_words = {}
matching_reg_words = {}

def fill_dict(crossword_dict):
    for i in range(len(cuts)):
        for j in range(len(cuts[i])):
            if cuts[i][j] != -1:
                if crossword_dict[i][0][cuts[j][i]] != ".":
                    w = crossword_dict[j][0]
                    w = w[:cuts[i][j]] + crossword_dict[i][0][cuts[j][i]] + w[cuts[i][j] + 1:]
                    crossword_dict[j] = w, crossword_dict[j][1], crossword_dict[j][2]

    return crossword_dict

def find_min(crossword_dict):
    min_pos = -1
    c = 0
    for t in crossword_dict:
        if crossword_dict[t][0].count(".") / len(crossword_dict[t][0]) != 0:
            if c == 0:
                min_word = crossword_dict[t][0].count(".") / len(crossword_dict[t][0])
                min_pos = t
                c += 1
            elif crossword_dict[t][0].count(".") / len(crossword_dict[t][0]) < min_word:
                min_word = crossword_dict[t][0].count(".") / len(crossword_dict[t][0])
                min_pos = t
    if min_pos == -1:
        for t in sorted(crossword_dict):
            if isinstance(crossword_dict[t][2], int):
                crossword_dict[t] = original_cross_dict[t][0], crossword_dict[t][1], crossword_dict[t][2]
                for j in range(len(cuts[t])):
                    if cuts[t][j] != -1 and j > t:
                        crossword_dict[j] = original_cross_dict[j][0], crossword_dict[j][1], original_cross_dict[j][2]
                crossword_dict = fill_dict(crossword_dict)
                return t, crossword_dict
    return min_pos, crossword_dict


def matchings(crossword_dict, min_pos, counter):
    matching_words[counter] = []
    matching_reg_words[counter] = []
    for j in reversed(sorted(words)):
        l = list(sre_yield.AllStrings(words[j], max_count=5, charset=string.ascii_uppercase))
        for k in l:
            if re.match(r"^" + crossword_dict[min_pos][0] + "$", k):
                flag = False
                for m in range(len(cuts[min_pos])):
                    if cuts[min_pos][m] != -1:
                        if crossword_dict[m][0][cuts[min_pos][m]] != "." and \
                                crossword_dict[m][0][cuts[min_pos][m]] != k[cuts[m][min_pos]]:
                            flag = True
                if not flag:
                    if k not in matching_words[counter]:
                        matching_words[counter].append(k)
                        matching_reg_words[counter].append(j)
    return matching_words[counter], matching_reg_words[counter]


def crossword(crossword_dict, counter):

    min_pos, crossword_dict = find_min(crossword_dict)

    if not bool(words):
        return crossword_dict
    else:
        matching_words[counter], matching_reg_words[counter] = matchings(crossword_dict, min_pos, counter)

    i = 0
    if not matching_words[counter]:
        words[deleted_words[-1]] = original_words[deleted_words[-1]]
        del deleted_words[-1]
        crossword_dict[last_min[-1]] = original_cross_dict[last_min[-1]][0], crossword_dict[last_min[-1]][1], original_cross_dict[last_min[-1]][2]
        for t in crossword_dict.keys():
            if crossword_dict[t][0].count(".") / len(crossword_dict[t][0]) != 0:
                crossword_dict[t] = original_cross_dict[t][0], crossword_dict[t][1], crossword_dict[t][2]
        crossword_dict = fill_dict(crossword_dict)
        i = keep_pos[-1]
        counter -= 1
        if i != -1:
            min_pos = last_min[-1]
        else:
            for j in range(counter):
                words[deleted_words[-1]] = original_words[deleted_words[-1]]
                del deleted_words[-1]
                del last_min[-1]
                del keep_pos[-1]
                crossword_dict[last_min[-1]] = original_cross_dict[last_min[-1]][0], crossword_dict[last_min[-1]][1], \
                                               crossword_dict[last_min[-1]][2]
                for t in crossword_dict.keys():
                    if crossword_dict[t][0].count(".") / len(crossword_dict[t][0]) != 0:
                        crossword_dict[t] = original_cross_dict[t][0], crossword_dict[t][1], crossword_dict[t][2]
                crossword_dict = fill_dict(crossword_dict,)
                min_pos = last_min[-1]
                i = keep_pos[-1]
                counter -= 1
                if i != -1:
                    break

    if matching_reg_words[counter][i] in words.keys():
        crossword_dict[min_pos] = matching_words[counter][i], crossword_dict[min_pos][1], words[
            matching_reg_words[counter][i]]
        del words[matching_reg_words[counter][i]]
        deleted_words.append(matching_reg_words[counter][i])
    else:
        crossword_dict[min_pos] = matching_words[counter][i], crossword_dict[min_pos][1], crossword_dict[min_pos][2]
    for t in crossword_dict.keys():
        if crossword_dict[t][0].count(".") / len(crossword_dict[t][0]) != 0:
            crossword_dict[t] = original_cross_dict[t][0], crossword_dict[t][1], crossword_dict[t][2]
    crossword_dict = fill_dict(crossword_dict)

    i += 1
    if min_pos not in last_min:
        last_min.append(min_pos)
        if i <= len(matching_words[counter]) - 1:
            keep_pos.append(i)
        else:
            keep_pos.append(-1)
    else:
        if i <= len(matching_words[counter]) - 1:
            keep_pos[-1] = i
        else:
            keep_pos[-1] = -1
    crossword(crossword_dict, counter + 1)


crossword(crossword_dict, counter)
for i in sorted(crossword_dict.keys()):
    print(i, crossword_dict[i][2], crossword_dict[i][0])
