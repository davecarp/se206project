from Tkinter import *

import operator
import random
import logging

import tkFileDialog
import tkMessageBox
import tkSimpleDialog

from spellorama.views import ListEditorView, new_word_prompt
from spellorama.tts import Festival
from spellorama.tldr import parse_tldr, gen_tldr

class ListEditorController(object):
    def __init__(self, view):
        self.tts = Festival()
        self.tts.start()
        self.bind(view)

    def on_left_list_select(self):
        self.view.center_list.model.clear()

        for selection in self.view.left_list.listbox.curselection():
            for word in self.view.left_list.model.get_value_by_index(int(selection)):
                self.view.center_list.model[word.word] = word
        self.view.center_list.listbox.select_set(0, END)
        self.on_center_list_select()
        self.refresh_transfer_strip()

    def on_center_list_select(self):
        if self.view.center_list.model or self.view.right_list.model:
            selection = self.view.center_list.listbox.curselection()
            if selection:
                self.view.word_properties.display(
                    [ self.view.center_list.model.get_value_by_index(int(i))
                    for i in selection ]
                    )
            self.refresh_transfer_strip()
        else:
            self.view.word_properties.display([])
        

    def on_right_list_select(self):
        if self.view.center_list.model or self.view.right_list.model:
            selection = self.view.right_list.listbox.curselection()
            print len(selection)
            if selection:
                self.view.word_properties.display(
                    [ self.view.right_list.model.get_value_by_index(int(i))
                      for i in selection ]
                )
            self.refresh_transfer_strip()
        else:
            self.view.word_properties.display([])

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
        self.on_center_list_select()

    def on_remove_all_button(self):
        self.view.right_list.model.clear()
        self.refresh_transfer_strip()
        self.on_center_list_select()

    def on_speak_button(self):
        self.tts.panic()
        self.tts.speak(". ".join(word.word
                                for word in self.view.word_properties.model))

    def on_panic_button(self):
        self.tts.panic()

    def on_import_button(self):
        filenames = tkFileDialog.askopenfilenames(filetypes=[("Word List", ".tldr")])

        for filename in filenames:
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
        self.refresh_transfer_strip()

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
        self.refresh_transfer_strip()

    def on_export_button(self):
        filename = tkFileDialog.asksaveasfilename(filetypes=[("Word List", ".tldr")])
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
            self.view.transfer_strip.create_random_button['state'] = NORMAL
        else:
            self.view.transfer_strip.add_all_button['state'] = DISABLED
            self.view.transfer_strip.create_random_button['state'] = DISABLED

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
                                    lambda _: self.on_left_list_select())

        view.center_list.listbox.bind("<<ListboxSelect>>",
                                      lambda _: self.on_center_list_select(y))

        view.right_list.listbox.bind("<<ListboxSelect>>",
                                     lambda _: self.on_right_list_select())

        view.toolkit.import_button['command'] = self.on_import_button
        view.toolkit.create_button['command'] = self.on_create_button
        view.toolkit.export_button['command'] = self.on_export_button

        view.transfer_strip.add_button['command'] = self.on_add_button
        view.transfer_strip.add_all_button['command'] = self.on_add_all_button
        view.transfer_strip.remove_button['command'] = self.on_remove_button
        view.transfer_strip.remove_all_button['command'] = self.on_remove_all_button
        view.transfer_strip.create_random_button['command'] = self.on_random_button

        view.word_properties.speak_button['command'] = self.on_speak_button
        view.word_properties.panic_button['command'] = self.on_panic_button
