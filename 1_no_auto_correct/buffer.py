"""
Contains the most basic text buffer,
this will simply append and pop characters from a list.
"""


class Text:
    def __init__(self) -> None:
        self.buffer: list[int] = []

    def add_char(self, c: int) -> None:
        self.buffer.append(c)

    def del_char(self) -> None:
        if len(self.buffer) > 0:
            self.buffer.pop()

    def del_word(self) -> None:
        if len(self.buffer) > 0 and self.buffer[-1] == ord(" "):
            self.buffer.pop()
        while len(self.buffer) > 0 and self.buffer[-1] != ord(" "):
            self.buffer.pop()

    def get_normal_text(self) -> list[int]:
        return self.buffer

    def get_dimmed_text(self) -> list[int]:
        return []
