import curses


def ctrl(c: int) -> int:
    """Returns the version of char with control pressed."""
    return (c) & 0x1F


def main(window: curses.window) -> None:
    curses.raw()
    buffer: list[int] = []
    window.clear()
    # curses.init_pair(1, 243, curses.COLOR_BLACK)
    # stdscreen.addstr("predict the input", curses.color_pair(1))
    while True:
        c = window.getch()
        if c == ctrl(ord("q")):
            break
        elif c == curses.KEY_BACKSPACE:
            try:
                buffer.pop()
            except IndexError:
                pass
        else:
            buffer.append(c)
        write_line = "".join([chr(c) for c in buffer])
        window.clear()
        window.addstr(write_line)


curses.wrapper(main)
