import curses


def ctrl(c: int) -> int:
    """Returns the version of char with control pressed."""
    return (c) & 0x1F


def buffer_to_string(buffer: list[list[int]], active: list[int]) -> str:
    output: list[str] = []
    for word in buffer:
        for c in word:
            output.append(chr(c))
        output.append(" ")
    for c in active:
        output.append(chr(c))
    return "".join(output)


def main(window: curses.window) -> None:
    curses.raw()
    buffer: list[list[int]] = []
    active: list[int] = []
    window.clear()
    # curses.init_pair(1, 243, curses.COLOR_BLACK)
    # stdscreen.addstr("predict the input", curses.color_pair(1))
    while True:
        c = window.getch()
        if c == ctrl(ord("q")):
            break
        elif c == ord(" "):
            buffer.append(active)
            active = []
        elif c == curses.KEY_BACKSPACE:
            try:
                active.pop()
            except IndexError:
                try:
                    active = buffer.pop()
                except IndexError:
                    pass
        elif c == 8:
            if len(active) > 0:
                active = []
            else:
                buffer.pop()
        elif c == curses.KEY_LEFT:
            if len(active) > 0:
                active = []
            else:
                buffer.pop()
        else:
            active.append(c)
        window.clear()
        window.addstr(buffer_to_string(buffer, active))


curses.wrapper(main)
