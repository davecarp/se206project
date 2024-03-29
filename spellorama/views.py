from Tkinter import *
import time

from models import Word
  
class AddWordDialog(Toplevel):
    """
    A dialog box used to create new words.
    """
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.word = None
        self.title("Add New Word")
        self.create_widgets()
        self.word_entry.focus()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.grab_set()
        self.wait_window(self)

    def done(self):
        """
        Called when the OK button is pressed -- creates a Word if possible,
        otherwise returns None.
        """
        if self.word_entry.get():
            self.word = Word(self.word_entry.get(),
                             self.definition_entry.get(),
                             self.example_entry.get(),
                             self.difficulty_entry.get())
        self.destroy()

    def create_widgets(self):
        """
        Create widgets to populate the window.
        """
        self.resizable(0, 0)

        for i, label_text in enumerate([ "Word", "Definition", "Example",
                                         "Difficulty "]):
            label = Label(self, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky=W)

        self.word_entry = Entry(self)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)
        self.word_entry.bind("<Return>", lambda _: self.done)

        self.definition_entry = Entry(self)
        self.definition_entry.grid(row=1, column=1, padx=5, pady=5)
        self.definition_entry.bind("<Return>", lambda _: self.done)

        self.example_entry = Entry(self)
        self.example_entry.grid(row=2, column=1, padx=5, pady=5)
        self.example_entry.bind("<Return>", lambda _: self.done)

        self.difficulty_entry = StringVar("")

        difficulty_menu = OptionMenu(self, self.difficulty_entry,
                                     "", "CL1", "CL2", "CL3", "CL4", "CL5",
                                     "CL6", "CL7", "CL8", "AL1", "AL2")
        difficulty_menu.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        frame = Frame(self)
        frame.grid(row=4, column=0, columnspan=2)

        self.ok_button = Button(frame, text="OK", command=self.done)
        self.ok_button.pack(side=LEFT)

        self.cancel_button = Button(frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

def new_word_prompt():
    """
    Convenient method for adding words and getting the word returned.
    """
    return AddWordDialog().word

class AssociativeListBoxStore(dict):
    """
    A backing store for a Listbox that is represented as a dictionary -- the
    keys are the items in the list and the values can be retrieved from the
    store.
    """
    def __init__(self, *args, **kwargs):
        self.binding = None
        self._ordering = []
        dict.__init__(self, *args, **kwargs)

    def bind(self, binding):
        """
        Bind a Listbox to the store.
        """
        self.binding = binding

        for k, v in list(self.items()):
            # somewhat disgusting, but works relatively well
            self[k] = v

    def get_value_by_index(self, index):
        """
        Get a value by ordering index.
        """
        return self[self._ordering[index]]

    def get_key_by_index(self, index):
        """
        Get a key by ordering index.
        """
        return self._ordering[index]

    def __setitem__(self, key, value):
        """
        Override for __setitem__ that adds an entry in the ordering list if
        required.
        """
        if self.binding is not None:
            if key not in self:
                self._ordering.append(key)
                self.binding.insert(END, key)

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        """
        Override for __delitem__ that updates the ordering list.
        """
        # lookup + delete from the ordering list is O(n), but it's better than
        # reordering a dictionary after every delete
        if self.binding is not None:
            key_index = self._ordering.index(key)
            self.binding.delete(key_index)

            del self._ordering[key_index]

        dict.__delitem__(self, key)

    def clear(self):
        """
        Override for clear that empties the ordering list.
        """
        self._ordering = []
        self.binding.delete(0, END)
        dict.clear(self)

class WordListWidget(Frame):
    """
    A scrollable Listbox widget for storing words.
    """
    def __init__(self, model, master=None, text=None):
        Frame.__init__(self, master)
        self.text = text
        self.pack()
        self.create_widgets()

        self.model = model
        self.model.bind(self.listbox)

    def create_widgets(self):
        """
        Populate with widgets.
        """
        if self.text is not None:
            self.label = Label(self, text=self.text, relief=SUNKEN)
            self.label.pack(side=TOP, fill=X)

        self.list_frame = Frame(self)
        self.list_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.list_frame,
                               yscrollcommand=self.scrollbar.set,
                               exportselection=False,
                               selectmode=EXTENDED)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar.config(command=self.listbox.yview)

class TransferStripWidget(Frame):
    """
    A widget with add, add all, add random, remove and remove all buttons.
    """
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Create a new frame which will hold the buttons that allow the user to
        add or remove single or multiple words.
        """
        self.add_button = Button(self, text=">")
        self.add_all_button = Button(self, text=">>")
        self.create_random_button = Button(self, text="Generate\nRandom List")
        self.remove_button = Button(self, text="<")
        self.remove_all_button = Button(self, text="<<")

        self.buttons = [ self.add_button, self.add_all_button,
                         self.create_random_button, self.remove_button,
                         self.remove_all_button ]

        # Set all buttons to be the same width have the same amount of padding 
        # in the x direction so that they will line up.
        for button in self.buttons:
            button['width'] = 11
            button.pack(side=TOP, pady=5)
            button['state'] = DISABLED

class WordPropertiesWidget(Frame):
    """
    A widget used to display the details of a word.
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.display([])

    def display(self, words):
        """
        Display a given word.
        """
        self.model = words

        if len(words) == 0:
            self.word_label['text'] = "(no words selected)"
            self.definition_label['text'] = ""
            self.example_label['text'] = ""
            self.difficulty_label['text'] = ""
        elif len(words) == 1:
            word = words[0]

            self.word_label['text'] = word.word or "(word not available)"
            self.definition_label['text'] = word.definition or "(no definition available)"
            self.example_label['text'] = word.example or "(no example available)"
            self.difficulty_label['text'] = word.difficulty or "(difficulty not available)"
        else:
            # then it's probably a word list
            self.word_label['text'] = "({0} words selected)".format(len(words))
            self.definition_label['text'] = ""
            self.example_label['text'] = ""
            self.difficulty_label['text'] = ""

    def create_widgets(self):
        """
        Populate with widgets.
        """
        self.word_frame = Frame(self)
        self.word_frame.grid(row=0, column=0, columnspan=3, sticky=W + E)

        self.word_label = Label(self.word_frame, text="",
                                font="TkDefaultFont 14 bold")
        self.word_label.pack(side=LEFT)

        for i, label_text in enumerate([ "Definition", "Example",
                                         "Difficulty" ]):
            label = Label(self, text=label_text, font="TkDefaultFont 9 bold",
                          justify=LEFT)
            label.grid(row=i + 1, column=0, sticky=W)

        self.definition_label = Label(self, text="")
        self.definition_label.grid(row=1, column=1, sticky=W)

        self.example_label = Label(self, text="")
        self.example_label.grid(row=2, column=1, sticky=W)

        self.difficulty_label = Label(self, text="")
        self.difficulty_label.grid(row=3, column=1, sticky=W)

        self.speak_button = Button(self.word_frame, text=u"\u25b6", bg="green")
        self.speak_button.pack(side=LEFT)

        self.panic_button = Button(self.word_frame, text=u"\u25a0", bg="red")
        self.panic_button.pack(side=LEFT)

class ToolkitWidget(Frame):
    """
    Toolbar widget.
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Populate with toobar buttons.
        """
        self.return_button = Button(self, text="Return to Teacher Menu")
        self.import_button = Button(self, text="Import List")
        self.export_button = Button(self, text="Export List")
        self.create_button = Button(self, text="Create New Word")        

        for x in [ self.return_button, self.import_button,
                   self.export_button, self.create_button ]:
            x.pack(side=LEFT, fill=X, expand=True)

class ListEditorView(Frame):
    """
    Main widget for the Teacher list editor view.
    """
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Create the elements of the Teacher list editor.
        """
        self.create_root_frames()
        self.create_left_list()
        self.create_center_list()
        self.create_transfer_buttons()
        self.create_right_list()

    def create_root_frames(self):
        """
        Set the two main frames. The bottom (word_properties_frame) one holds
        the properties of a word (i.e. meaning, context etc), and the top one
        holds everything else.
        """
        self.toolkit = ToolkitWidget(self)
        self.pane = PanedWindow(self, orient=VERTICAL, sashrelief=SUNKEN)

        self.toolkit.pack(side=TOP, fill=X)
        self.pane.pack(side=TOP, fill=BOTH, expand=True)

        self.top_pane = PanedWindow(self.pane, orient=HORIZONTAL,
                                    sashrelief=SUNKEN)
        self.word_properties = WordPropertiesWidget(self.pane)

        self.pane.add(self.top_pane, stretch="always")
        self.pane.add(self.word_properties, stretch="never")

    def create_left_list(self):
        """
        Create the left list.
        """
        self.left_list = WordListWidget(AssociativeListBoxStore(),
                                        self.top_pane,
                                        text="Word Lists")
        self.top_pane.add(self.left_list, stretch="always", padx=5)

    def create_center_list(self):
        """
        Create the center list.
        """
        self.center_list = WordListWidget(AssociativeListBoxStore(),
                                          self.top_pane,
                                          text="Words in List")
        self.top_pane.add(self.center_list, stretch="always", padx=5)

    def create_transfer_buttons(self):
        """
        Create the buttons between the center and right list.
        """
        self.transfer_strip = TransferStripWidget(self.top_pane)
        self.top_pane.add(self.transfer_strip, stretch="never", padx=5,
                          sticky=W + E)

    def create_right_list(self):
        """
        Create the right list.
        """
        self.right_list = WordListWidget(AssociativeListBoxStore(),
                                         self.top_pane,
                                         text="Selected Words")
        self.top_pane.add(self.right_list, stretch="always", padx=5)

if __name__ == '__main__':
    root = Tk()
    app = ListEditorView(master=root)
    app.pack(fill=BOTH, expand=True)
    app.mainloop()
