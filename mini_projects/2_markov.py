"""Make the methods that train a markov model on the TEST_CORPUS and return the possible next words after an input word."""

from dataclasses import dataclass

TEST_CORPUS = """One factor often overlooked when trying to raise standards is the spelling systems of languages , which can make it very hard for some children to learn to read and write .
Victory was surely hers .
Planning for a retirement overseas , though , is difficult when currencies may fluctuate wildly over a few years .
Even the researchers on this study say the findings should be taken with caution .
Jankovic was No. 1 for a week this summer , but she got there without winning a tournament .
More likely he will be out for the remainder of 2010 .
Truth is not belief .
The factory is due to close with the loss of 163 jobs .
Held in Stoke Park near Guildford , the event has been running since 1992 .
Before that he was a consultant at McKinsey and Bain & Co .
The spelling systems help with writing papers ."""


@dataclass
class WordEntry:
    count: int
    next: dict[str, int]


class MarkovModel:
    def __init__(self) -> None:
        self.bigrams: dict[str, WordEntry] = {}

    def _prepare_corpus(self, text: str) -> list[str]:
        return text.lower().split()

    def _add_bigram(self, first_word: str, next_word: str):
        """Fill in the method to add combinations of words (bigrams) to the model"""
        pass 

    def train_on_corpus(self, text: str) -> None:
        """This method iterates over all words, and feeds the current and next word to the model."""
        corpus = self._prepare_corpus(text)
        for i in range(len(corpus) - 1):
            self._add_bigram(corpus[i], corpus[i + 1])

    def get_next_words(self, word: str) -> list[tuple[str, float]]:
        next_words = []
        """Fill in the method to get the next words and calculate their probability."""
        return next_words


def main():
    markov = MarkovModel()
    markov.train_on_corpus(TEST_CORPUS)
    suggestions = markov.get_next_words("the")
    assert ("spelling", 0.25) in suggestions

if __name__ == "__main__":
    main()
