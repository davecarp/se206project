# http://effbot.org/tkinterbook/+
from Tkinter import *

from spellorama.tldr import parse_tldr, gen_tldr
from spellorama.models import Word

class ListBoxModel(dict):
    def __init__(self, *args, **kwargs):
        self.binding = None
        self._ordering = []
        dict.__init__(self, *args, **kwargs)

    def bind(self, binding):
        self.binding = binding

        for k, v in list(self.items()):
            # somewhat disgusting, but works relatively well
            self[k] = v

    def get_by_index(self, index):
        return self[self._ordering[index]]

    def __setitem__(self, key, value):
        if self.binding is not None:
            if key not in self:
                self._ordering.append(key)
                self.binding.insert(len(self._ordering), key)

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        # lookup + delete from the ordering list is O(n), but it's better than
        # reordering a dictionary after every delete
        if self.binding is not None:
            key_index = self._ordering.index(key)
            self.binding.delete(key_index)

            del self._ordering[key_index]

        dict.__delitem__(self, key)

    def clear(self):
        self._ordering = []
        self.binding.delete(0, END)
        dict.clear(self)

class WordListWidget(Frame):
    def __init__(self, model, master=None, text=None):
        Frame.__init__(self, master)
        self.text = text
        self.pack()
        self.create_widgets()

        self.model = model
        self.model.bind(self.listbox)

    def create_widgets(self):
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
                               selectmode=MULTIPLE)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar.config(command=self.listbox.yview)

class TransferStripWidget(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.disable()

    def create_widgets(self):
        # Create a new frame which will hold the buttons that allow the user 
        # to add or remove single or multiple words.
        self.add_word = Button(self, text=">")
        self.add_all_words = Button(self, text=">>")
        self.remove_word = Button(self, text="<")
        self.remove_all_words = Button(self, text="<<")

        self.buttons = [ self.add_word, self.add_all_words, self.remove_word,
                       self.remove_all_words ]

        # Set all buttons to be the same width have the same amount of padding 
        # in the x direction so that they will line up.
        for button in self.buttons:
            button['width'] = 5
            button.pack(side=TOP, pady=5)

    def enable(self):
        for button in self.buttons:
            button["state"] = NORMAL

    def disable(self):
        for button in self.buttons:
            button["state"] = DISABLED

class WordPropertiesWidget(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.display([])

    def display(self, words):
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
        self.word_label = Label(self, text="",
                                font="TkDefaultFont 14 bold")

        self.word_label.grid(row=0, column=0, columnspan=2, sticky=W)

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

class ToolkitWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        for x in ["Import List", "Create New Word", "Create Random List",
                  "Export List"]:
            x = Button(self, text=x)
            x.pack(side=LEFT, fill=X, expand=True)

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
        self.toolkit = ToolkitWidget(self)
        self.pane = PanedWindow(self, orient=VERTICAL, sashrelief=SUNKEN)

        self.toolkit.pack(side=TOP, fill=X)
        self.pane.pack(side=TOP, fill=BOTH, expand=True)

        self.top_pane = PanedWindow(self.pane, orient=HORIZONTAL, sashrelief=SUNKEN)
        self.word_properties = WordPropertiesWidget(self.pane)

        self.pane.add(self.top_pane, stretch="always")
        self.pane.add(self.word_properties, stretch="never")

    def _on_center_list_select(self, e):
        selection = e.widget.curselection()
        if selection:
            self.transfer_strip.enable()
            self.word_properties.display(
                [ self.center_list.model.get_by_index(int(i)) for i in selection ]
            )
        else:
            self.transfer_strip.disable()

    def _on_left_list_select(self, e):
        self.center_list.model.clear()

        for selection in e.widget.curselection():
            for word in self.left_list.model.get_by_index(int(selection)):
                self.center_list.model[word.word] = word

    def create_left_list(self):
        self.left_list = WordListWidget(ListBoxModel(), self.top_pane,
                                        text="Word Lists")
        self.top_pane.add(self.left_list, stretch="always", padx=5)
        self.left_list.listbox.bind("<<ListboxSelect>>",
                                    self._on_left_list_select)

    def create_center_list(self):
        self.center_list = WordListWidget(ListBoxModel(), self.top_pane,
                                          text="Words in List")
        self.center_list.listbox.bind("<<ListboxSelect>>",
                                      self._on_center_list_select)
        self.top_pane.add(self.center_list, stretch="always", padx=5)

    def create_transfer_buttons(self):
        self.transfer_strip = TransferStripWidget(self.top_pane)
        self.top_pane.add(self.transfer_strip, stretch="never", padx=5,
                          sticky=W + E)

    def create_right_list(self):
        self.right_list = WordListWidget(ListBoxModel(), self.top_pane,
                                         text="Selected Words")
        self.top_pane.add(self.right_list, stretch="always", padx=5)

if __name__ == '__main__':
    root = Tk()
    app = ListEditorView(master=root)
    app.pack(fill=BOTH, expand=True)
    app.mainloop()
