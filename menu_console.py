
from lcd_menu import Command, MenuItem, Menu
import curses

class ConsoleRadioMenu(Menu):
    '''A curses menu example for receiving input and displaying the menu on the console'''

    def __init__(self):

        # standard curses init
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
    
        # our example menu definition
        items = [
            MenuItem("Playlists", refresh_callback=self.load_playlists),
            MenuItem("Radio", [
                MenuItem("Radio Station 1"),
                MenuItem("Radio Station 2"),
                MenuItem("Radio Station 3")
            ]),
            MenuItem("Settings", [
                MenuItem("IP Address"),
                MenuItem("Shutdown"),
            ]),
            Command("Volume UP", self.volume_up),
            Command("Volume DOWN", self.volume_down)
        ]

        # pass all this to the base class
        return super(ConsoleRadioMenu, self).__init__(items, self.update)

    def loop(self):
        '''Main application loop. Receives input and dispatches one of either "up", "down", "select" or "back" commands.'''
        
        while 1:
            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.up()
            if c == curses.KEY_DOWN:
                self.down()
            if c == 8:  # backspace
                self.back()
            if c == 10: # enter
                self.select()
            if c == ord('q'):
                break  

    def update(self, menu):
        '''Called to draw the current menu view.'''
        self.stdscr.clear() 

        i = 0        
        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                self.stdscr.addstr(i, 0, ">> " + item.title + " <<") 
            else:
                self.stdscr.addstr(i, 0, item.title) 
            i+=1


    def volume_up(self, item, arg):
        print "RUNNING COMMAND: VOLUME UP"

    def volume_down(self, item, arg):
        print "RUNNING COMMAND: VOLUME DOWN"

    def on_play(self, item, arg):
        print "RUNNING COMMAND: PLAY: " + item.title

    def load_playlists(self, item, arg):
        '''Example of a dynamic menu item callback'''
    
        items = []

        items.append(Command("Andrew's Fairly Long Playlist", self.on_play))
        items.append(Command("Dynamic 2", self.on_play))
        items.append(Command("Dynamic 3", self.on_play))
        items.append(Command("Dynamic 4", self.on_play))
        
        return items
