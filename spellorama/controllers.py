from Tkinter import *

import operator
import random
import logging

import tkFileDialog
import tkMessageBox
import tkSimpleDialog

from spellorama.models import Word
from spellorama.views import ListEditorView
from spellorama.tldr import parse_tldr, gen_tldr

class AddWordDialog(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.word = None
        self.title("Add New Word")
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.grab_set()
        self.wait_window(self)

    def done(self):
        if self.word_entry.get():
            self.word = Word(self.word_entry.get(),
                             self.definition_entry.get(),
                             self.example_entry.get(),
                             self.difficulty_entry.get())
        self.destroy()

    def create_widgets(self):
        self.resizable(0, 0)

        for i, label_text in enumerate([ "Word", "Definition", "Example",
                                         "Difficulty "]):
            label = Label(self, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky=W)

        self.word_entry = Entry(self)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)

        self.definition_entry = Entry(self)
        self.definition_entry.grid(row=1, column=1, padx=5, pady=5)

        self.difficulty_entry = Entry(self)
        self.difficulty_entry.grid(row=2, column=1, padx=5, pady=5)

        self.example_entry = Entry(self)
        self.example_entry.grid(row=3, column=1, padx=5, pady=5)

        frame = Frame(self)
        frame.grid(row=4, column=0, columnspan=2)

        self.ok_button = Button(frame, text="OK", command=self.done)
        self.ok_button.pack(side=LEFT)

        self.cancel_button = Button(frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

def new_word_prompt():
    return AddWordDialog().word

class ListEditorController(object):
    def __init__(self, view):
        self.bind(view)

    def on_left_list_select(self, e):
        self.view.center_list.model.clear()

        for selection in e.widget.curselection():
            for word in self.view.left_list.model.get_value_by_index(int(selection)):
                self.view.center_list.model[word.word] = word
        self.refresh_transfer_strip()

    def on_center_list_select(self, e):
        selection = e.widget.curselection()
        if selection:
            self.view.word_properties.display(
                [ self.view.center_list.model.get_value_by_index(int(i))
                  for i in selection ]
            )
        self.refresh_transfer_strip()

    def on_right_list_select(self, e):
        selection = e.widget.curselection()
        if selection:
            self.view.word_properties.display(
                [ self.view.right_list.model.get_value_by_index(int(i))
                  for i in selection ]
            )
        self.refresh_transfer_strip()

    def on_add_button(self):
        selection = self.view.center_list.listbox.curselection()
        for index in selection:
            key = self.view.center_list.model.get_key_by_index(int(index))
            word = self.view.center_list.model[key]
            self.view.right_list.model[key] = word
        self.refresh_transfer_strip()

    def on_add_all_button(self):
        for k, v in self.view.center_list.model.iteritems():
            self.view.right_list.model[k] = v
        self.refresh_transfer_strip()

    def on_remove_button(self):
        selection = self.view.right_list.listbox.curselection()
        for index in selection:
            key = self.view.right_list.model.get_key_by_index(int(index))
            del self.view.right_list.model[key]
        self.refresh_transfer_strip()

    def on_remove_all_button(self):
        self.view.right_list.model.clear()
        self.refresh_transfer_strip()

    def on_import_button(self):
        for filename in tkFileDialog.askopenfilenames():
            try:
                with open(filename, "r") as f:
                    data = list(parse_tldr(f))
            except IOError as e:
                tkMessageBox.showwarning(
                    "Import Error",
                    "Could not open {0}".format(filename)
                )
                logging.warn(e)
            except Exception as e:
                tkMessageBox.showwarning(
                    "Import Error",
                    "Could not parse {0}".format(filename)
                )
                logging.warn(e)
            else:
                self.view.left_list.model[filename] = data

    def on_create_button(self):
        word = new_word_prompt()
        if word is not None:
            self.view.right_list.model[word.word] = word

    def on_random_button(self):
        num = tkSimpleDialog.askinteger("Generate Random List",
                                        "How many items should the list have?")
        if not num: return

        words = list(self.view.center_list.model.values())
        random.shuffle(words)

        while num > 0 and words:
            word = words.pop()
            self.view.right_list.model[word.word] = word
            num -= 1

    def on_export_button(self):
        filename = tkFileDialog.asksaveasfilename()
        if not filename: return

        try:
            with open(filename, "w") as f:
                for line in gen_tldr(sorted(list(self.view.right_list.model.values()),
                                            key=operator.attrgetter("word"))):
                    f.write(line)
        except IOError as e:
            tkMessageBox.showwarning(
                "Export Error",
                "Could not save {0}".format(filename)
            )
            logging.warn(e)

        tkMessageBox.showinfo(
            "Export",
            "Exported successfully to {0}".format(filename)
        )

    def refresh_transfer_strip(self):
        if self.view.center_list.model:
            self.view.transfer_strip.add_all_button['state'] = NORMAL
        else:
            self.view.transfer_strip.add_all_button['state'] = DISABLED

        if self.view.right_list.model:
            self.view.transfer_strip.remove_all_button['state'] = NORMAL
        else:
            self.view.transfer_strip.remove_all_button['state'] = DISABLED

        if self.view.center_list.listbox.curselection():
            self.view.transfer_strip.add_button['state'] = NORMAL
        else:
            self.view.transfer_strip.add_button['state'] = DISABLED

        if self.view.right_list.listbox.curselection():
            self.view.transfer_strip.remove_button['state'] = NORMAL
        else:
            self.view.transfer_strip.remove_button['state'] = DISABLED

    def bind(self, view):
        self.view = view

        view.left_list.listbox.bind("<<ListboxSelect>>",
                                    self.on_left_list_select)

        view.center_list.listbox.bind("<<ListboxSelect>>",
                                      self.on_center_list_select)

        view.right_list.listbox.bind("<<ListboxSelect>>",
                                     self.on_right_list_select)

        view.toolkit.import_button['command'] = self.on_import_button
        view.toolkit.create_button['command'] = self.on_create_button
        view.toolkit.random_button['command'] = self.on_random_button
        view.toolkit.export_button['command'] = self.on_export_button

        view.transfer_strip.add_button['command'] = self.on_add_button
        view.transfer_strip.add_all_button['command'] = self.on_add_all_button
        view.transfer_strip.remove_button['command'] = self.on_remove_button
        view.transfer_strip.remove_all_button['command'] = self.on_remove_all_button

if __name__ == '__main__':
    root = Tk()
    view = ListEditorView(master=root)
    controller = ListEditorController(view)
    view.pack(fill=BOTH, expand=True)
    root.mainloop()

