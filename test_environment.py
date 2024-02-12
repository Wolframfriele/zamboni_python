import curses
from difflib import ndiff


class Spellcheck:
    def __init__(self) -> None:
        self.dictionary = self.__read_word_list()

    def __levenshtein_distance(
        self,
        str1: str,
        str2: str,
    ) -> int:
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

    def __similarity(self, str1: str, str2: str) -> float:
        return 1 - (self.__levenshtein_distance(str1, str2) / min(len(str1), len(str2)))

    def __read_word_list(self) -> list[str]:
        with open("big_wordlist.txt") as f:
            return f.read().split()

    def get_match(self, word: list[int]) -> list[int]:
        converted_word = "".join([chr(c) for c in word])
        if converted_word in self.dictionary:
            return word
        matches: list[tuple[float, str]] = []
        for potential in self.dictionary:
            if abs(len(word) - len(potential)) <= 2:
                dist = self.__similarity(converted_word, potential)
                if dist > 0.5:
                    matches.append((dist, potential))
        if len(matches) > 0:
            matches = sorted(matches, key=lambda x: x[0])
            str_word = matches[0][1]
            return [ord(c) for c in str_word]
        else:
            return word


class Text:
    def __init__(self) -> None:
        self.autocorrect = Spellcheck()
        self.buffer: list[int] = []
        self.active: list[int] = []
        self.nearest: list[int] = []

    def add_char(self, c: int) -> None:
        if c == ord(" "):
            if len(self.nearest) > 0:
                for i in self.nearest:
                    self.buffer.append(i)
            else:
                for i in self.active:
                    self.buffer.append(i)
            self.buffer.append(c)
            self.active = []
            self.nearest = []
        else:
            self.active.append(c)
            self.nearest = self.autocorrect.get_match(self.active)

    def del_char(self) -> None:
        if len(self.active) > 0:
            try:
                self.active.pop()
                if len(self.active) > 0:
                    self.nearest = self.autocorrect.get_match(self.active)
            except IndexError:
                pass
        else:
            try:
                self.buffer.pop()
            except IndexError:
                pass

    def del_word(self) -> None:
        if len(self.active) > 0:
            self.active = []
            self.nearest = []
        else:
            try:
                last_char = 0
                while last_char != ord(" "):
                    last_char = self.buffer.pop()
            except IndexError:
                pass

    def get_normal_text(self) -> list[int]:
        return self.buffer

    def get_dimmed_text(self) -> list[int]:
        return self.nearest


class Terminal:
    def __init__(self, buff: Text) -> None:
        self.buff = buff
        self.window: curses.window
        self._stopped = False

    @staticmethod
    def __init_curses() -> None:
        curses.raw()
        curses.init_pair(1, 243, curses.COLOR_BLACK)

    def run(self, window: curses.window) -> None:
        self.window = window
        self.__init_curses()
        while not self._stopped:
            self.__handle_input()
            self.__draw_screen()

    def __handle_input(self) -> None:
        c = self.window.getch()
        if c == self.__ctrl(ord("q")):
            self._stopped = True
        elif c == curses.KEY_BACKSPACE:
            self.buff.del_char()
        elif c == 8:
            self.buff.del_word()
        else:
            self.buff.add_char(c)

    def __draw_screen(self) -> None:
        self.window.erase()
        for i in self.buff.get_normal_text():
            self.window.addch(i)
        for i in self.buff.get_dimmed_text():
            self.window.addch(i, curses.color_pair(1))

    @staticmethod
    def __ctrl(c: int) -> int:
        """Returns the version of char with control pressed."""
        return (c) & 0x1F


if __name__ == "__main__":
    buffer = Text()
    term = Terminal(buffer)
    curses.wrapper(term.run)
