"""
This script returns the edit distance between two words.
It prints the dynamic programming table to gain insight into
how the algorithm determines the edit distance.
"""


def print_word(word: str) -> None:
    print("    ", end="")
    for char in word:
        print(f", {char}", end="")
    print("")


def edit_distance(str1: str, str2: str) -> int:
    print_word(str1)
    current = [i for i in range(len(str1) + 1)]
    previous = current.copy()
    print(f"  {current}")
    for i in range(1, len(str2) + 1):
        previous = current
        current[0] = i
        for j in range(1, len(str1) + 1):
            if str1[j - 1] != str2[i - 1]:
                insert = previous[j]
                replace = previous[j - 1]
                delete = current[j - 1]
                minimum = min(insert, replace, delete) + 1
            else:
                minimum = previous[j - 1]
            current[j] = minimum
        print(f"{str2[i-1]} {current}")
    return current[len(str1)]


if __name__ == "__main__":
    word1 = "ruust"
    word2 = "rust"

    edit_distance(word1, word2)
    print("")
