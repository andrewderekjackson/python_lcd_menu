import os

class ConsoleDisplayController(object):

    def update(self, menu):

        os.system('cls')
        
        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                print ">> " + item.title + " <<"
            else:
                print "   " + item.title


