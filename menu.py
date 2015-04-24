import msvcrt, os


class MenuItem(object):

    def __init__(self, title, items=None, command=None):
        self._title = title
        self._items = items
        self._command = command

    @property
    def title(self):
        return self._title

    @property
    def items(self):
        return self._items

    def invoke_command(self):
        if self._command is not None:
            self._command

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
        self.main_menu = items
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
        if self.current_menu.selected_item.invoke_command():
            return

        if self.current_menu.selected_item.items is not None:
            # add current menu to history
            self._history.append(self.current_menu)
            self.current_menu = Menu(self.current_menu.selected_item.items)

    def back(self):

        if len(self._history) > 0:
            self.current_menu = self._history.pop()


def volume_up():
    print "VOLUME UP"

def volume_down():
    print "VOLUME DOWN"

main_menu = Menu([
    MenuItem("Playlists", [
        MenuItem("Playlist 1"),
        MenuItem("Playlist 2"),
        MenuItem("Playlist 3")
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
    MenuItem("Volume UP", volume_up),
    MenuItem("Volume DOWN", volume_down)

])

menuController = MenuController(main_menu)



while True:
    os.system('cls')
    menuController.draw()

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
                menuController.up()
                continue

            if ord(ky) == 80: # down
                menuController.down()
                continue

            if ord(ky) == 13: #enter
                menuController.select()
                continue

            if ord(ky) == 8: # backspace
                menuController.back()
                continue
