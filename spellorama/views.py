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
        a.pack(side=LEFT)
        # Create a new frame which will hold the list of words, a scrollbar 
        # attached to it and the create word button. This will then have two 
        # subframes, one for the list and scrollbar and one for the button.
        b = ListViewer(self.top_frame)
        b.pack(side=LEFT)
        # Create a new frame which will hold the buttons that allow the user 
        # to add or remove single or multiple words.
        self.buttons_frame = Frame(self.top_frame)
        self.buttons_frame.pack(side=LEFT)
        buttons = ["Add", "Add All", "Remove", "Remove All"]
        for button in buttons:
            button = Button(text=button)
            button.pack(side=TOP)
            button['width'] = 10
            button['padx'] = 0
        
        c = ListViewer(self.top_frame)
        c.pack(side=LEFT)

class ListViewer(Frame):

    def __init__(self, master):
        self.list_view_frame = Frame(master)
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
        
        
