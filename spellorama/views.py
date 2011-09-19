# http://effbot.org/tkinterbook/+
from Tkinter import *

class ListView(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.list_frame = Frame(self)
        self.list_frame.pack(side=TOP)

        self.button_frame = Frame(self)
        self.button_frame.pack(side=BOTTOM)

        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.list_frame,
                               yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH)

        self.scrollbar.config(command=self.listbox.yview)

class TransferStrip(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create a new frame which will hold the buttons that allow the user 
        # to add or remove single or multiple words.
        self.add_word = Button(self, text=">")
        self.add_word.pack(side=TOP)

        self.add_all_words = Button(self, text=">>")
        self.add_all_words.pack(side=TOP)

        self.remove_word = Button(self, text="<")
        self.remove_word.pack(side=TOP)

        self.remove_all_words = Button(self, text="<<")
        self.remove_all_words.pack(side=TOP)

        # Set all buttons to be the same width have the same amount of padding 
        # in the x direction so that they will line up.
        for button in [ self.add_word, self.add_all_words, self.remove_word,
                       self.remove_all_words ]:
            button['width'] = 10
            button['padx'] = 0

class ListEditorView(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.create_root_frames()
        self.create_left_list()
        self.create_center_list()
        self.create_transfer_buttons()
        self.create_right_list()

    def create_root_frames(self):
        # Set the two main frames. The bottom (word_properties_frame) one holds
        # the properties of a word (i.e. meaning, context etc), and the top one
        # holds everything else.
        self.top_frame = Frame(self)
        self.word_properties_frame = Frame(self)
        self.top_frame.pack(side=TOP)
        self.word_properties_frame.pack(side=BOTTOM)

    def create_left_list(self):
        self.left_list_view = ListView(self.top_frame)
        self.left_list_view.pack(side=LEFT)

        self.import_button = Button(self.left_list_view.button_frame,
                                    text="Import...")
        self.import_button.pack(side=BOTTOM)

    def create_center_list(self):
        self.center_list_view = ListView(self.top_frame)
        self.center_list_view.pack(side=LEFT)

        self.createword_button = Button(self.center_list_view.button_frame, 
                                        text="Create New Word")
        self.createword_button.pack()

    def create_transfer_buttons(self):
        self.transfer_strip = TransferStrip(self.top_frame)
        self.transfer_strip.pack(side=LEFT)

    def create_right_list(self):
        self.right_list_view = ListView(self.top_frame)
        self.right_list_view.pack(side=LEFT)

        self.export_button = Button(self.right_list_view.button_frame,
                                    text="Export")
        self.export_button.pack()

if __name__ == '__main__':
    root = Tk()
    app = ListEditorView(master=root)
    app.mainloop()
