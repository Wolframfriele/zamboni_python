from time import perf_counter
from buffer.markov_model import Markov


class SpellingCorrection:
    def __init__(self) -> None:
        store_model_path = "../data/markov_model.msgpack"
        training_data_path = "../data/1-billion-word/training"
        self.markov = Markov(store_model_path, training_data_path)

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

    def __similarity_score(self, str1: str, str2: str, probability: float) -> float:
        distance = self.edit_distance(str1, str2)
        if str1[0] != str2[0]:
            distance += 0.3
        return (1 / distance) + probability

    def get_match(self, word: str, previous_word: str | None) -> str:
        if word:
            if previous_word:
                next_words = self.markov.get_next_words(previous_word)
            else:
                next_words = self.markov.get_next_words(".")
            if word in next_words:
                return word
            matches: list[tuple[float, str]] = []
            for potential_word, probability in next_words.items():
                if abs(len(word) - len(potential_word)) <= 2:
                    dist = self.__similarity_score(word, potential_word, probability)
                    matches.append((dist, potential_word))
            if len(matches) > 0:
                matches = sorted(matches, key=lambda x: x[0], reverse=True)
                #print(matches)
                return matches[0][1]
        return word


def measure_correction_duration():
    prev_word = "most"
    word = "boisterus"
    check = SpellingCorrection()
    start = perf_counter()
    corrected = check.get_match(word, prev_word)
    duration = perf_counter() - start
    print(f"Using new edit distance Correction: {corrected}, took: {duration}s")


if __name__ == "__main__":
    measure_correction_duration()
