
import msvcrt
from commands import InputCommand

class InputController(object):



    def __init__(self, callback):
        self._callback = callback

    def loop(self):

        while True:

            ky = msvcrt.getch()
            length = len(ky)
            if length != 0:
                # send events to event handling functions
                if ky == " ":
                    raise SystemExit
                else:
                    if ky == '\x00' or ky == '\xe0':
                        ky = msvcrt.getch()

                    if ord(ky) == 72: #up
                        self._callback(InputCommand.UP)
                        continue

                    if ord(ky) == 80: # down
                        self._callback(InputCommand.DOWN)
                        continue

                    if ord(ky) == 13: #enter
                        self._callback(InputCommand.SELECT)
                        continue

                    if ord(ky) == 8: # backspace
                        self._callback(InputCommand.BACK)
                        continue


