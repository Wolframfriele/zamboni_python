import os
import pickle
from time import perf_counter
from dataclasses import dataclass

import msgspec

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


class WordStruct(msgspec.Struct):
    word: str
    count: int
    next: dict[int, int]


class MarkovModel(msgspec.Struct):
    max_id: int
    word_index: dict[str, int]
    words: dict[int, WordStruct]


class Markov:
    def __init__(self, store_model_path: str, training_data_path: str) -> None:
        self.model_path = store_model_path
        self.model: MarkovModel
        if os.path.exists(store_model_path):
            self._load_model(store_model_path)
        else:
            self.model = MarkovModel(0, {}, {})
            self.train(training_data_path)

    def _load_model(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = msgspec.msgpack.decode(f.read(), type=MarkovModel)

    def _store_model(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def _load_corpus(self, path: str) -> list[str]:
        with open(path, encoding="utf8") as f:
            return f.read().translate(TRANSLATE_TABLE).lower().split()

    @staticmethod
    def _contains_number(word: str) -> bool:
        return any(map(str.isdigit, word))

    def _add_word(self, word: str) -> None:
        self.model.max_id += 1
        self.model.word_index[word] = self.model.max_id
        self.model.words[self.model.max_id] = WordStruct(word, 0, {})

    def _add_bigram(self, first_word: str, next_word: str) -> None:
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
        if first_word not in self.model.word_index:
            self._add_word(first_word)
        if next_word not in self.model.word_index:
            self._add_word(next_word)
        first_word_index = self.model.word_index[first_word]
        next_word_index = self.model.word_index[next_word]
        # increase the counter for the current word
        self.model.words[first_word_index].count += 1
        # increase the counter for the next word
        self.model.words[first_word_index].next[next_word_index] = (
            self.model.words[first_word_index].next.get(next_word_index, 0) + 1
        )

    def _train_on_corpus(self, corpus: list[str]) -> None:
        for i in range(len(corpus) - 1):
            self._add_bigram(corpus[i], corpus[i + 1])

    def train(self, training_data_folder_path: str) -> None:
        start = perf_counter()
        for path in os.listdir(training_data_folder_path):
            print(path)
            corpus_path = training_data_folder_path + "/" + path
            self._train_on_corpus(self._load_corpus(corpus_path))
        duration = perf_counter() - start
        print(f"Training took {duration}s")
        self._store_model(self.model_path)

    def get_next_words(self, word: str) -> dict[str, float]:
        """
        Checks the next words for a word.
        """
        next_words = {}
        if self._contains_number(word):
            word = "0"
        if word in self.model.word_index:
            word_index = self.model.word_index[word]
            current_word = self.model.words[word_index]
            for key, count in current_word.next.items():
                word_probability = count / current_word.count
                next_words[self.model.words[key].word] = word_probability
        else:
            for return_word in self.model.words.values():
                word_probability = return_word.count / self.model.max_id
                next_words[return_word.word] = word_probability
        return next_words
    
    def match_index(self, word: str):
        idx = self.model.word_index[word]
        word_data = self.model.words[idx]
        return (idx, word_data.word, word_data.count, len(word_data.next))


if __name__ == "__main__":
    store_model_path = "data/markov_model.msgpack"

    training_data_path = "data/1-billion-word/training"

    start = perf_counter()
    markov = Markov(store_model_path, training_data_path)
    duration = perf_counter() - start
    print(f"Loading took {duration}s")

    # start = perf_counter()
    # markov.convert_to_msgspec("data/markov_model.msgpack")
    # duration = perf_counter() - start
    # print(f"Storing msgspec took {duration}s")

    # print(markov.get_next_words("."))

    print("what" in markov.get_next_words("."))
    # print(markov.match_index("blasphemous"))

    # unique_words = len(markov.model.word_index)
    # print(f"Amount of entries in model: {unique_words}")

    # counter = 0
    # for word in markov.model.words.values():
    #     if word.count < 10:
    #         # print(word.word)
    #         counter += 1

    # print(f"Words with only one occurrence: {counter}")
    # print(f"Words after pruning: {unique_words - counter}")
