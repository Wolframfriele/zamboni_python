class Markov:
    def __init__(self) -> None:
        self.word_list = self.__read_word_list()
        self.dictionary = {
            "test": [],
            "best": [],
            "rest": [],
        }

    def __read_word_list(self) -> list[str]:
        with open("../data/wordlist.txt") as f:
            return f.read().split()


markov = Markov()
index_of = markov.word_list.index("rest")
print(index_of)
print(len(markov.word_list))
