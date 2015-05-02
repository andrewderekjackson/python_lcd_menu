import curses
from commands import InputCommand

class CursesInputController(object):

    def __init__(self, callback):
        self._callback = callback

    def loop(self):

        # init
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(1)

            while 1:
                c = stdscr.getch()
                if c == curses.KEY_UP:
                    self._callback(InputCommand.UP)
                if c == curses.KEY_DOWN:
                    self._callback(InputCommand.DOWN)
                if c == ord('b'):
                    self._callback(InputCommand.BACK)
                if c == ord('s'):
                    self._callback(InputCommand.SELECT)
                if c == ord('q'):
                    break  # Exit the while()

        finally:
            # cleanup
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()




