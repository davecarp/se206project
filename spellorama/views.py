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
        self.top_left_frame = Frame(self.top_frame)
        self.top_left_frame.pack(side=LEFT)
        self.left_list_frame = Frame(self.top_left_frame)
        self.left_list_frame.pack(side=TOP)
        self.left_button_frame = Frame(self.top_left_frame)
        self.left_button_frame.pack(side=BOTTOM)                
        self.lol_scrollbar = Scrollbar(self.left_list_frame)
        self.lol_scrollbar.pack(side=RIGHT, fill=Y)
        self.list_of_lists = Listbox(self.left_list_frame,
                                     yscrollcommand=self.lol_scrollbar.set)
        self.list_of_lists.pack(side=LEFT, fill=BOTH)
        for x in range(1,101):
            self.list_of_lists.insert(END, x)
        self.lol_scrollbar.config(command=self.list_of_lists.yview)
        self.import_button = Button(self.left_button_frame, text="Import...")
        self.import_button.pack(side=BOTTOM)
        # Create a new frame which will hold the list of words, a scrollbar 
        # attached to it and the create word button. This will then have two 
        # subframes, one for the list and scrollbar and one for the button.
        self.top_midleft_frame = Frame(self.top_frame)
        self.top_midleft_frame.pack(side=LEFT)
        self.midleft_list_frame = Frame(self.top_midleft_frame)
        self.midleft_list_frame.pack(side=TOP)
        self.midleft_button_frame = Frame(self.top_midleft_frame)
        self.midleft_button_frame.pack(side=BOTTOM)
        self.low_scrollbar = Scrollbar(self.midleft_list_frame)
        self.low_scrollbar.pack(side=RIGHT, fill=Y)
        self.list_of_words = Listbox(self.midleft_list_frame,
                                     yscrollcommand=self.low_scrollbar.set)
        self.list_of_words.pack(side=LEFT, fill=BOTH)
        for x in range(1,101):
            self.list_of_words.insert(END, x)
        self.low_scrollbar.config(command=self.list_of_words.yview)
        self.createword_button = Button(self.midleft_button_frame, 
                                        text="Create New Word")
        self.createword_button.pack()
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
        self.top_right_frame = Frame(self.top_frame)
        self.top_right_frame.pack(side=LEFT)
        self.tldr_list_frame = Frame(self.top_right_frame)
        self.tldr_list_frame.pack(side=TOP)
        self.export_button_frame = Frame(self.top_right_frame)
        self.export_button_frame.pack(side=BOTTOM)
        self.tldr_scrollbar = Scrollbar(self.tldr_list_frame)
        self.tldr_scrollbar.pack(side=RIGHT, fill=Y)
        self.tldr_list = Listbox(self.tldr_list_frame,
                                 yscrollcommand=self.tldr_scrollbar.set)
        self.tldr_list.pack(side=LEFT, fill=BOTH)
        for x in range (1,101):
            self.tldr_list.insert(END, x)
        self.tldr_scrollbar.config(command=self.tldr_list.yview)
        self.export_button = Button(self.export_button_frame, text="Export")
        self.export_button.pack()
        

root = Tk()
app = ListEditorView(master=root)
app.mainloop()
root.destroy()
        
        
