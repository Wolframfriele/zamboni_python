from difflib import ndiff


def levenshtein_distance(
    str1,
    str2,
):
    counter = {"+": 0, "-": 0}
    distance = 0
    for edit_code, *_ in ndiff(str1, str2):
        if edit_code == " ":
            distance += max(counter.values())
            counter = {"+": 0, "-": 0}
        else:
            counter[edit_code] += 1
    distance += max(counter.values())
    return distance


def similarity(str1, str2):
    return 1 - (levenshtein_distance(str1, str2) / min(len(str1), len(str2)))


def read_word_list() -> list[str]:
    with open("wordlist.txt") as f:
        return f.read().split()


def potential_matches(word, dictionary):
    matches: list[tuple[float, str]] = []
    for potential in dictionary:
        dist = similarity(word, potential)
        if dist > 0.5:
            matches.append((dist, potential))
    return sorted(matches, key=lambda x: x[0])


wordlist = read_word_list()
print(potential_matches("tst", wordlist))
# print(levenshtein_distance("t", "the"))
