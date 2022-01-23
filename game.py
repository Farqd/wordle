import random
import sys
import itertools
import time
import statistics

def read_words():
    with open("in") as f:
        return [x.strip() for x in f if len(x.strip()) == 5]


def check(word, guess):
    # (index, color, letter)
    ret = []
    ix = 0
    for (w, g) in zip(word, guess):
        if w == g:
            ret.append((ix, 'green', g))
        elif g in word:
            ret.append((ix, 'yellow', g))
        else:
            ret.append((ix, 'black', g))
        ix += 1
    return ret


def good_guess_single(response, guess):
    for (ix, color, letter) in response:
        if color == 'black' and letter in guess:
            return False
        if color == 'green' and guess[ix] != letter:
            return False
        if color == 'yellow':
            if letter not in guess or guess[ix] == letter:
                return False
    return True


def good_guess(responses, guess):
    if responses == []:
        return True
    return min(good_guess_single(response, guess) for response in responses) == 1


def process_guess(guess):
    global results

    # print(word, guess)
    result = check(word, guess)
    results.append(result)
    correct_letters = sum(1 if color == 'green' else 0 for _, color, _ in result)
    # if correct_letters == 5:
        # print("SUCCESS")
        # for x in results:
        #     print(x)
        # exit(0)
    return correct_letters == 5


def from_input():
    for line in sys.stdin:
        guess = line.strip()
        print(good_guess(results, guess))

# prep = ['dwine', 'louts', 'grapy']

# (19130, 'arose')
# (11133, 'until')
# (5868, 'dumpy')
word = ''
results = []
words = read_words()

def solve():
    global word
    global results

    word = random.choice(words)
    # print(word)
    results = []
    prep = ['arose', 'until']#, 'dumpy']
    # arose
    # unlit
    # dumpy
    prep = ['arose', 'unlit'] # , 'dumpy'] #, 'whack', 'befog']
    # prep = ['adits', 'enrol']
    for w in prep:
        # assert(good_guess(results, w))
        process_guess(w)

    while(True):
        new_word = random.choice(words)
        # print(new_word)
        if good_guess(results, new_word):
            # print(new_word)
            if process_guess(new_word):
                return results
        # time.sleep(2)
    return len(results)

# CT = 500
# O = [solve() for i in range(CT)]
# print(statistics.mean(len(x) for x in O))
# print(sum(1 if len(x) <= 6 else 0 for x in O) / CT)
# print(statistics.mean(len(solve()) for i in range(100)))

# exit(0)

def do_prep():
    global word
    global results
    word = random.choice(words)
    results = []

    prep = ['arose', 'unlit', 'dumpy'] #, 'whack', 'befog']
    for w in prep:
        process_guess(w)


def check_remaining(old_remaining):
    global word
    global results
    new_remaining = [w for w in old_remaining if good_guess(results, w)]
    # print("Correct word:", word)
    # print("Hardcoded guesses:", prep)
    # print("Remaining words:", len(remaining), remaining)
    assert(word in new_remaining)
    return new_remaining


def find_optimal(remaining):
    global results
    global word
    tmp_results = results
    proper_answer = word

    max_len = 100000000
    best_guess = ''

    sample_set = remaining # if len(remaining) <= 30 else random.sample(remaining, 30)
    # print(sample_set)
    for new_word in sample_set:

        max_tmp = 0
        for what_if_answer in sample_set:
            word = what_if_answer
            process_guess(new_word)
            rem_len = len(check_remaining(remaining))
            max_tmp = max(max_tmp, rem_len)
            # print(new_word, what_if_answer, max_tmp)
            results.pop()

        if max_tmp < max_len:
            max_len = max_tmp
            best_guess = new_word

    word = proper_answer
    assert results == tmp_results
    # print(len(results))
    # print(max_len, best_guess)
    return best_guess



def solve_2():
    do_prep()
    print("Word:", word)
    remaining = words

    def run_once(remaining):
        new_remaining = check_remaining(remaining)
        # print("Remaining: ", len(remaining))
        # print(remaining)
        # for r in results:
        #     print(r)
        optimal_word = find_optimal(new_remaining)
        # print("Optimal word", optimal_word)
        if process_guess(optimal_word):
            # print("Print success", len(results))
            return (new_remaining, True)
        return (new_remaining, False)

    while True:
        (remaining, success) = run_once(remaining)
        if success:
            return results


CT = 500
O = [solve_2() for i in range(CT)]
print(statistics.mean(len(x) for x in O))
print(sum(1 if len(x) <= 6 else 0 for x in O) / CT)
