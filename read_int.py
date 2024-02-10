import curses


def main(window: curses.window) -> None:
    curses.raw()
    buffer: list[list[int]] = []
    active: list[int] = []
    window.clear()
    # curses.init_pair(1, 243, curses.COLOR_BLACK)
    # stdscreen.addstr("predict the input", curses.color_pair(1))
    while True:
        c = window.getch()
        if c == ord("q"):
            break
        else:
            active.append(c)
        window.clear()
        window.addstr("".join([str(c) for c in active]))


curses.wrapper(main)
