import random
from string import ascii_lowercase

def read_words():
    with open("in") as f:
        return [x.strip() for x in f if len(x.strip()) == 5]



letter_ranking = {c : 0 for c in ascii_lowercase}
letter_rankings = [{c : 0 for c in ascii_lowercase} for i in range(5)]
words = read_words()

# print(letter_rankings[0])
for i in range(5):
    for word in words:
        for l in word:
            letter_rankings[i][l] += 1

print(letter_rankings)
print(len(words))

for i in range(5):
    candidate = ''
    max_val = 0
    for word in words:
        if len(''.join(set(word))) != 5:
            continue
        val = sum( letter_rankings[ix][val] for (ix, val) in enumerate(word) )
        if val > max_val:
            candidate = word
            max_val = val

    for l in candidate:
        for i in range(5):
            # print(l, i)
            letter_rankings[i][l] = 0

    print(candidate)


exit(0)
for i in range(3):
    candidates = [(sum(letter_ranking[l] for l in ''.join(set(word))), word) for word in words]
    w = max(candidates)
    print(w)
    for l in w[1]:
        letter_ranking[l] = 0
