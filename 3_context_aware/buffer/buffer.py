from buffer.spelling_correction import SpellingCorrection


class Text:
    def __init__(self) -> None:
        self.autocorrect = SpellingCorrection()
        self.buffer: list[int] = []
        self.active: list[int] = []
        self.capitalize_next = True

    def _get_last_word(self) -> str | None:
        if self.buffer:
            end = len(self.buffer)
            if self.buffer[-1] == ord(" "):
                end -= 1
            start = end - 1

            while start - 1 > 0:
                if (
                    self.buffer[start - 1] == ord(" ")
                    or self.buffer[start] == ord(".")
                    or self.buffer[start] == ord("?")
                    or self.buffer[start] == ord("!")
                    or self.buffer[start] == ord(":")
                    or self.buffer[start] == ord(";")
                    or self.buffer[start] == ord(",")
                    or self.buffer[start] == ord("/")
                ):
                    break
                start -= 1
            return "".join([chr(c) for c in self.buffer[start:end]]).lower()
        return None

    def _check_active(self) -> None:
        converted_to_str = "".join([chr(c) for c in self.active]).lower()
        matched_word = self.autocorrect.get_match(
            converted_to_str, self._get_last_word()
        )

        if self.capitalize_next and self.active:
            matched_word = matched_word.capitalize()
            self.capitalize_next = False

        if matched_word == "i":
            matched_word = "I"
        elif matched_word == "i'm":
            matched_word = "I'm"

        for i in matched_word:
            self.buffer.append(ord(i))
        self.active = []

    def add_char(self, c: int) -> None:
        if c == ord(" ") or c == ord(",") or c == ord(":") or c == ord(";"):
            self._check_active()
            self.buffer.append(c)
        elif c == ord(".") or c == ord("!") or c == ord("?") or c == ord(";"):
            self._check_active()
            self.buffer.append(c)
            self.capitalize_next = True
        else:
            self.active.append(c)

    def del_char(self) -> None:
        if len(self.active) > 0:
            self.active.pop()
        elif len(self.buffer) > 0:
            self.buffer.pop()

    def del_word(self) -> None:
        if len(self.active) > 0:
            self.active = []
        else:
            if len(self.buffer) > 0 and self.buffer[-1] == ord(" "):
                self.buffer.pop()
            while len(self.buffer) > 0 and self.buffer[-1] != ord(" "):
                self.buffer.pop()

    def get_normal_text(self) -> list[int]:
        return self.buffer

    def get_dimmed_text(self) -> list[int]:
        return self.active

