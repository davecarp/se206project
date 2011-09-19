# http://effbot.org/tkinterbook/+
from Tkinter import *

class ListEditorView(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Teacher Interface")
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        # Set the two main frames. The bottom (word_properties_frame) one holds
        # the properties of a word (i.e. meaning, context etc), and the top one
        # holds everything else.
        self.top_frame = Frame(self)
        self.word_properties_frame = Frame(self)
        self.top_frame.pack(side=TOP)
        self.word_properties_frame.pack(side=BOTTOM)
        # Create a new frame which will hold the list of lists, a scrollbar 
        # attached to it and the import button. This will then have two 
        # subframes, one for the list and scrollbar and one for the button.
        a = ListViewer(self.top_frame)
        # Create a new frame which will hold the list of words, a scrollbar 
        # attached to it and the create word button. This will then have two 
        # subframes, one for the list and scrollbar and one for the button.
        b = ListViewer(self.top_frame)
        # Create a new frame which will hold the buttons that allow the user 
        # to add or remove single or multiple words.
        self.top_midright_frame = Frame(self.top_frame)
        self.top_midright_frame.pack(side=LEFT)
        self.add_word = Button(self.top_midright_frame, text="Add")
        self.add_word.pack(side=TOP)
        self.add_all_words = Button(self.top_midright_frame, text="Add All")
        self.add_all_words.pack(side=TOP)
        self.remove_word = Button(self.top_midright_frame, text="Remove")
        self.remove_word.pack(side=TOP)
        self.remove_all_words = Button(self.top_midright_frame, 
                                       text="Remove All")
        self.remove_all_words.pack(side=TOP)
        list_of_buttons = [self.add_word, self.add_all_words, self.remove_word,
                           self.remove_all_words]
        # Set all buttons to be the same width have the same amount of padding 
        # in the x direction so that they will line up.
        for button in list_of_buttons:
            button['width'] = 10
            button['padx'] = 0
        # Create a last frame which will hold the list of words that the .tldr 
        # will be comprised of and the export button. There will be subfolders
        c = ListViewer(self.top_frame)

class ListViewer(object):

    def __init__(self, master):
        self.list_view_frame = Frame(master)
        self.list_view_frame.pack(side=LEFT)
        self.list_scrollbar = Scrollbar(self.list_view_frame)
        self.list_scrollbar.pack(side=RIGHT, fill=Y)
        self.list_table = Listbox(self.list_view_frame, 
                                  yscrollcommand=self.list_scrollbar.set)
        self.list_table.pack(side=LEFT, fill=BOTH)
        self.list_scrollbar.config(command=self.list_table.yview)
        for x in range(1,101):
            self.list_table.insert(END, x)
        

root = Tk()
app = ListEditorView(master=root)
app.mainloop()
root.destroy()
        
        
