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
        if first_word in self.bigrams:
            self.bigrams[first_word].count += 1
            if next_word in self.bigrams[first_word].next:
                self.bigrams[first_word].next[next_word] += 1
            else:
                self.bigrams[first_word].next[next_word] = 1
        else:
            self.bigrams[first_word] = WordEntry(1, {next_word: 1})

    def train_on_corpus(self, text: str) -> None:
        corpus = self._prepare_corpus(text)
        for i in range(len(corpus) - 1):
            self._add_bigram(corpus[i], corpus[i + 1])

    def get_next_words(self, word: str) -> list[tuple[str, float]]:
        next_words = []
        if word in self.bigrams:
            for possible_next_word, next_word_count in self.bigrams[word].next.items():
                word_probability = next_word_count/  self.bigrams[word].count
                next_words.append((possible_next_word, word_probability))
        else:
            total_word_count = len(self.bigrams)
            for possible_next_word, next_word_entry in self.bigrams.items():
                word_probability = next_word_entry.count / total_word_count
                next_words.append((possible_next_word, word_probability))
        return next_words


def main():
    markov = MarkovModel()
    markov.train_on_corpus(TEST_CORPUS)
    suggestions = markov.get_next_words("the")
    assert ("spelling", 0.25) in suggestions

if __name__ == "__main__":
    main()
