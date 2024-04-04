import os
import pickle
from time import perf_counter
from dataclasses import dataclass

# "best setup" results in:
#
# word_index: {
#   "best": 1,
#   "setup": 2,
# }
# words = {
#   1: WordEntry(word="best", count=1, next: {2:1}),
#   2: WordEntry(word="setup", count=1, next: {})
# }
#
# If token contains a digit, store it in special digit WordEntry under the string "0"

TRANSLATE_TABLE = {
    ord("("): None,
    ord(")"): None,
    ord("'"): None,
    ord('"'): None,
    ord("/"): None,
}


@dataclass
class WordEntry:
    word: str
    count: int
    next: dict[int, int]


class Model:
    def __init__(self) -> None:
        self.max_index = 0
        self.words_index: dict[str, int] = {}
        self.words: dict[int, WordEntry] = {}

    @staticmethod
    def _contains_number(word: str) -> bool:
        return any(map(str.isdigit, word))

    def _add_word(self, word: str) -> None:
        self.max_index += 1
        self.words_index[word] = self.max_index
        self.words[self.max_index] = WordEntry(word, 0, {})

    def add_bigram(self, first_word: str, next_word: str) -> None:
        """
        Adds words to the markov model, when a word is already in the model,
        the count will be increased.

        If the word contains a number, the word will be stored under '0', this
        helps with containing context for those kind of tokens. Without requiring
        every possible number.
        """
        if self._contains_number(first_word):
            first_word = "0"
        if self._contains_number(next_word):
            next_word = "0"
        if first_word not in self.words_index:
            self._add_word(first_word)
        if next_word not in self.words_index:
            self._add_word(next_word)
        first_word_index = self.words_index[first_word]
        next_word_index = self.words_index[next_word]
        # increase the counter for the current word
        self.words[first_word_index].count += 1
        # increase the counter for the next word
        self.words[first_word_index].next[next_word_index] = (
            self.words[first_word_index].next.get(next_word_index, 0) + 1
        )

    def get_next_words(self, word: str) -> list[tuple[str, float]]:
        """
        Checks if word exists in 
        """
        next_words = []
        if self._contains_number(word):
            word = "0"
        if word in self.words_index:
            word_index = self.words_index[word]
            current_word = self.words[word_index]
            for key, count in current_word.next.items():
                word_probability = count / current_word.count
                next_words.append((self.words[key].word, word_probability))
        else:
            for return_word in self.words.values():
                word_probability = return_word.count / self.max_index
                next_words.append((return_word.word, word_probability))
        return next_words



class Markov:
    def __init__(self, store_model_path: str, training_data_path: str) -> None:
        self.model_path = store_model_path
        self.model = Model() 
        if os.path.exists(store_model_path):
            self._load_model(store_model_path)
        else:
            self.train(training_data_path)

    def _load_model(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)

    def _store_model(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def _load_corpus(self, path: str) -> list[str]:
        with open(path, encoding="utf8") as f:
            return f.read().translate(TRANSLATE_TABLE).lower().split()

    def _train_on_corpus(self, corpus: list[str]) -> None:
        for i in range(len(corpus) - 1):
            self.model.add_bigram(corpus[i], corpus[i + 1])

    def train(self, training_data_folder_path: str) -> None:
        start = perf_counter()
        for path in os.listdir(training_data_folder_path):
            print(path)
            corpus_path = training_data_folder_path + "/" + path
            self._train_on_corpus(self._load_corpus(corpus_path))
        duration = perf_counter() - start
        print(f"Training took {duration}s")
        self._store_model(self.model_path)

    def get_next(self, word: str) -> list[tuple[str, float]]:
        return self.model.get_next_words(word)


if __name__ == "__main__":
    store_model_path = "data/markov_model.pickle"
    training_data_path = "data/1-billion-word/training"

    start = perf_counter()
    markov = Markov(store_model_path, training_data_path)
    duration = perf_counter() - start
    print(f"Loading took {duration}s")

    unique_words = len(markov.model.words_index)
    print(f"Amount of entries in model: {unique_words}")

    counter = 0
    for word in markov.model.words.values():
        if word.count < 10:
            #print(word.word)
            counter += 1
    
    print(f"Words with only one occurrence: {counter}")
    print(f"Words after pruning: {unique_words - counter}")

    #start = perf_counter()
    #print(markov.get_next("i"))
    #duration = perf_counter() - start
    print(f"Prediction took {duration}s")
