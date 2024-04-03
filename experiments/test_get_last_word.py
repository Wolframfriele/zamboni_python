def get_last_word(buffer: list[int]) -> str | None:
    if buffer:
        end = len(buffer)
        if buffer[-1] == ord(" "):
            end -= 1
        start = end - 1

        while start - 1 > 0:
            if (
                buffer[start - 1] == ord(" ")
                or buffer[start] == ord("?")
                or buffer[start] == ord("!")
                or buffer[start] == ord(":")
                or buffer[start] == ord(";")
                or buffer[start] == ord(",")
                or buffer[start] == ord("/")
            ):
                break
            start -= 1
        return "".join([chr(c) for c in buffer[start:end]]).lower()
    return None


def test_buffer():
    fake_buffer = [ord(x) for x in ""]
    print(f"'{get_last_word(fake_buffer)}'")


if __name__ == "__main__":
    test_buffer()
