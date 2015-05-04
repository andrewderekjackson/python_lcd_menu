import os

class MenuItem(object):
    '''A single menu item which can contain child menu items'''

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
    '''A single menu item which executes a callback when selected'''

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


class MenuView(object):
    '''Represents a current menu level and tracks the selected item'''

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

    @property
    def items(self):
        return self._items

    def down(self):
        self.selected_index += 1

    def up(self):
        self.selected_index -= 1

    def refresh(self):
        self.selected_item.refresh()
        

    @property
    def selected_item(self):
        return self._items[self._selected_index]

class Menu(object):
    '''Base menu controller responsible for managing the menu'''

    def __init__(self, items, update):
        self._history = []
        self.main_menu = MenuView(items)
        self.current_menu = self.main_menu
        self.update = update

        self.update(self.current_menu)

    def up(self):
        self.current_menu.up()
        self.update(self.current_menu)

    def down(self):
        self.current_menu.down()
        self.update(self.current_menu)

    def select(self):

        if isinstance(self.current_menu.selected_item, Command):
            self.current_menu.selected_item.invoke_command()
            return

        if isinstance(self.current_menu.selected_item, MenuItem):

            self.current_menu.selected_item.refresh()

            if self.current_menu.selected_item.items is not None:

                # add current menu to history
                self._history.append(self.current_menu)
                self.current_menu = MenuView(self.current_menu.selected_item.items)
            
        self.update(self.current_menu)

    def back(self):

        if len(self._history) > 0:
            self.current_menu = self._history.pop()

        self.update(self.current_menu)

    def update(self):
        pass
