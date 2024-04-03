from time import perf_counter


class SpellingCorrection:
    def __init__(self, use_dict: bool = True) -> None:
        if use_dict:
            self.dictionary = self.__read_word_list()

    @staticmethod
    def edit_distance(str1: str, str2: str) -> int:
        current = [i for i in range(len(str1) + 1)]
        for i in range(1, len(str2) + 1):
            previous = current.copy()
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
        return current[len(str1)]

    def __read_word_list(self) -> list[str]:
        with open("../data/wordlist.txt") as f:
            return f.read().split()

    def __similarity_score(self, str1: str, str2: str) -> float:
        return 1 - (self.edit_distance(str1, str2) / min(len(str1), len(str2)))

    def get_match(self, word: str) -> str:
        if word:
            if word in self.dictionary:
                return word
            matches: list[tuple[float, str]] = []
            for potential in self.dictionary:
                if abs(len(word) - len(potential)) <= 2:
                    dist = self.__similarity_score(word, potential)
                    if dist > 0.5:
                        matches.append((dist, potential))
            if len(matches) > 0:
                matches = sorted(matches, key=lambda x: x[0])
                return matches[0][1]
        return word


def measure_correction_duration():
    word = "dependensies"
    check = SpellingCorrection()
    start = perf_counter()
    corrected = check.get_match(word)
    duration = perf_counter() - start
    print(f"Using new edit distance Correction: {corrected}, took: {duration}s")


if __name__ == "__main__":
    measure_correction_duration()
