import os

from input_curses import *
from display_ILI9341 import *
from commands import InputCommand


class MenuItem(object):

    def __init__(self, title, items=None, refresh_callback=None, refresh_callback_args = None):
        self._title = title
        self._items = items
        self._refresh_callback = refresh_callback
        self._refresh_callback_args = refresh_callback_args

    @property
    def title(self):
        return self._title

    @property
    def items(self):
        return self._items

    def refresh(self):
        if self._refresh_callback is not None:
            self._items = self._refresh_callback(self, self._refresh_callback_args)

class Command(MenuItem):

    def __init__(self, title, command, arg=None):
        MenuItem.__init__(self, title, None)

        self._command = command
        self._arg = arg

    def invoke_command(self):
        if self._command is not None:
            self._command(self, self._arg)
            return True
        return False

    def refresh(self):
        pass

class Menu(object):

    def __init__(self, items):
        self._selected_index = 0
        self._items = items

    @property
    def selected_index(self):
        return self._selected_index
    
    @property
    def items(self):
        return self._items

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

    def refresh(self):
        self.selected_item.refresh()
        

    @property
    def selected_item(self):
        return self._items[self._selected_index]



class MenuController(object):

    def __init__(self, items, display):
        self._history = []
        self.main_menu = Menu(items)
        self.current_menu = self.main_menu
        self.display = display

        self.display.update(self.current_menu)


    def up(self):
        self.current_menu.up()
        self.display.update(self.current_menu)

    def down(self):
        self.current_menu.down()
        self.display.update(self.current_menu)

    def select(self):

        if isinstance(self.current_menu.selected_item, Command):
            self.current_menu.selected_item.invoke_command()
            return

        if isinstance(self.current_menu.selected_item, MenuItem):

            self.current_menu.selected_item.refresh()

            if self.current_menu.selected_item.items is not None:

                # add current menu to history
                self._history.append(self.current_menu)
                self.current_menu = Menu(self.current_menu.selected_item.items)
            
        self.display.update(self.current_menu)

    def back(self):

        if len(self._history) > 0:
            self.current_menu = self._history.pop()

        self.display.update(self.current_menu)

    def input(self, command):
        if command == InputCommand.UP:
            self.up()
        if command == InputCommand.DOWN:
            self.down()
        if command == InputCommand.SELECT:
            self.select()
        if command == InputCommand.BACK:
            self.back()


def volume_up(item, arg):
    print "RUNNING COMMAND: VOLUME UP"


def volume_down(item, arg):
    print "RUNNING COMMAND: VOLUME DOWN"

def on_play(item, arg):
    print "RUNNING COMMAND: PLAY: " + item.title
    pass

def load_playlists(item, arg):
    
    items = []

    items.append(Command("Andrew's Fairly Long Playlist", on_play))
    items.append(Command("Dynamic 2", on_play))
    items.append(Command("Dynamic 3", on_play))
    items.append(Command("Dynamic 4", on_play))
        
    return items


main_menu = [
    MenuItem("Playlists", refresh_callback=load_playlists),
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

displayController = LcdDisplayController()
menuController = MenuController(main_menu, displayController)
inputController = CursesInputController(menuController.input)


inputController.loop()