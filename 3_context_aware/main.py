import curses
from buffer import Text


class Terminal:
    def __init__(self, buffer: Text) -> None:
        self.buffer = buffer
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
            self.buffer.del_char()
        elif c == 8:
            self.buffer.del_word()
        else:
            self.buffer.add_char(c)

    def __draw_screen(self) -> None:
        self.window.erase()
        for i in self.buffer.get_normal_text():
            self.window.addch(i)
        for i in self.buffer.get_dimmed_text():
            self.window.addch(i, curses.color_pair(1))

    @staticmethod
    def __ctrl(c: int) -> int:
        """Returns the version of char with control pressed."""
        return (c) & 0x1F


if __name__ == "__main__":
    buffer = Text()
    term = Terminal(buffer)
    curses.wrapper(term.run)
