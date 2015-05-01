

class DisplayController(object):

    def update(menu):

        os.system('cls')
        
        for (index, item) in enumerate(menu.items):
            if index == self.selected_index:
                print ">> " + item.title + " <<"
            else:
                print "   " + item.title
