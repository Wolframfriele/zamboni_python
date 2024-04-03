"""
This contains the code to interact with the terminal.
It relies on the cursus module. The text itself is stored
in the buffer.
"""

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
        """
        Start a new cursus window, this stores the state
        off the terminal and clear everything. Opening a
        new environment in raw mode.
        It then start's a controll loop that checks for user
        input, handles the input, and updates the screen.

        The curses.wrapper takes care of cleaning up raw mode
        and restoring the terminal to the original state when
        the command to exit the editor is received (ctrl + q).
        """
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
