import msvcrt, os


class MenuItem(object):

    def __init__(self, title, items=None):
        self._title = title
        self._items = items

    @property
    def title(self):
        return self._title

    @property
    def items(self):
        return self._items


class Command(MenuItem):

    def __init__(self, title, command, arg=None):
        MenuItem.__init__(self, title, None)

        self._command = command
        self._arg = arg

    def invoke_command(self):
        if self._command is not None:
            self._command(self._arg)

            print("Press any key to continue...")
            msvcrt.getch()

            return True

        return False

class Menu(object):

    def __init__(self, items):
        self._selected_index = 0
        self._items = items

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, val):
        if val >= len(self._items):
            self._selected_index = len(self._items)-1
        else:
            if val > 0:
                self._selected_index = val
            else:
                self._selected_index = 0


    def down(self):
        self.selected_index += 1

    def up(self):
        self.selected_index -= 1

    def draw(self):

        for (index, item) in enumerate(self._items):
            if index == self._selected_index:
                print ">> " + item.title + " <<"
            else:
                print "   " + item.title

    @property
    def selected_item(self):
        return self._items[self._selected_index]



class MenuController(object):

    def __init__(self, items):
        self._history = []
        self.main_menu = Menu(items)
        self.current_menu = self.main_menu

    def draw(self):
        self.current_menu.draw()

    def up(self):
        self.current_menu.up()
        self.draw()

    def down(self):
        self.current_menu.down()
        self.draw()

    def select(self):

        if isinstance(self.current_menu.selected_item, Command):
            self.current_menu.selected_item.invoke_command()
            return

        if isinstance(self.current_menu.selected_item, MenuItem):
            # add current menu to history

            self._history.append(self.current_menu)
            self.current_menu = Menu(self.current_menu.selected_item.items)

    def back(self):

        if len(self._history) > 0:
            self.current_menu = self._history.pop()


def volume_up(arg):
    print "RUNNING COMMAND: VOLUME UP"

def volume_down(arg):
    print "RUNNING COMMAND: VOLUME DOWN"

def on_play(arg):
    print "RUNNING COMMAND: PLAY: " + str(arg)
    pass


main_menu = [
    MenuItem("Playlists", [
        Command("Playlist 1", on_play, 1),
        Command("Playlist 1", on_play),
        Command("Playlist 1", on_play),
    ]),
    MenuItem("Radio", [
        MenuItem("Radio Station 1"),
        MenuItem("Radio Station 2"),
        MenuItem("Radio Station 3")
    ]),
    MenuItem("Settings", [
        MenuItem("IP Address"),
        MenuItem("Shutdown"),
    ]),
    Command("Volume UP", volume_up),
    Command("Volume DOWN", volume_down)
]

menuController = MenuController(main_menu)
menuController.select()
menuController.select()



#
#
# while True:
#     os.system('cls')
#     menuController.draw()
#
#     ky = msvcrt.getch()
#     length = len(ky)
#     if length != 0:
#         # send events to event handling functions
#         if ky == " ":
#             raise SystemExit
#         else:
#             if ky == '\x00' or ky == '\xe0':
#                 ky = msvcrt.getch()
#
#             if ord(ky) == 72: #up
#                 menuController.up()
#                 continue
#
#             if ord(ky) == 80: # down
#                 menuController.down()
#                 continue
#
#             if ord(ky) == 13: #enter
#                 menuController.select()
#                 continue
#
#             if ord(ky) == 8: # backspace
#                 menuController.back()
#                 continue
