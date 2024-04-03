import os
import pickle
from time import perf_counter


class Markov:
    def __init__(self, store_model_path: str, training_data_path: str) -> None:
        self.model_path = store_model_path
        self.store: dict[str, dict[str, int]] = {}
        if os.path.exists(store_model_path):
            self._load_model(store_model_path)
        else:
            self.train(training_data_path)

    def _load_model(self, path: str) -> None:
        with open(path, "rb") as f:
            self.store = pickle.load(f)

    def _store_model(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.store, f)

    def _load_corpus(self, path: str) -> list[str]:
        with open(path) as f:
            return f.read().lower().split()

    def _train_on_corpus(self, corpus: list[str]) -> None:
        for i in range(len(corpus) - 1):
            if corpus[i] in self.store:
                if corpus[i + 1] in self.store[corpus[i]]:
                    self.store[corpus[i]][corpus[i + 1]] += 1
                else:
                    self.store[corpus[i]][corpus[i + 1]] = 1
            else:
                self.store[corpus[i]] = {corpus[i + 1]: 1}

    def train(self, training_data_folder_path: str) -> None:
        start = perf_counter()
        for path in os.listdir(training_data_folder_path):
            corpus_path = training_data_folder_path + "/" + path
            self._train_on_corpus(self._load_corpus(corpus_path))
        duration = perf_counter() - start
        print(f"Training took {duration}s")
        self._store_model(self.model_path)

    def get_next(self, word: str) -> dict[str, int] | None:
        return self.store.get(word)


if __name__ == "__main__":
    store_model_path = "../../../data/markov_model.pickle"
    training_data_path = "../../../data/1-billion-word/training"

    start = perf_counter()
    markov = Markov(store_model_path, training_data_path)
    duration = perf_counter() - start
    print(f"Loading took {duration}s")

    print(f"Amount of entries in model: {len(markov.store)}")

    start = perf_counter()
    markov.get_next("resting")
    duration = perf_counter() - start
    print(f"Prediction took {duration}s")
