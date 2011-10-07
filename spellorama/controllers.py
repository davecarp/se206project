from Tkinter import *

import datetime
import os
import random
import logging

import teacher
from models import Word
import database

import tkFileDialog
import tkMessageBox
import tkSimpleDialog

from views import ListEditorView, new_word_prompt
from tts import Festival
from tldr import parse_tldr, gen_tldr


class ListEditorController(object):
    """ This class specifies the behavior for the ListEditor int the teacher
    interface. """

    def __init__(self, view):
        """ Initialisation method. Starts festival, binds this class to the
        ListEditor and then populates its list of lists with the pre-specified 
        lists. """
        self.tts = Festival()
        self.tts.start()
        self.bind(view)
        self.populate()

    def on_left_list_select(self):
        """ Method called when words are selected in the left list containing
        .tldr files that can be read from. """
        self.view.center_list.model.clear()
        for selection in self.view.left_list.listbox.curselection():
            for k, v in self.view.left_list.model.get_value_by_index(int(selection)).iteritems():
                self.view.center_list.model[k] = v
        self.view.center_list.listbox.select_set(0, END)
        self.on_center_list_select()
        self.refresh_transfer_strip()

    def on_center_list_select(self):
        """ Method called when words are selected in the center list containing 
        words in the currently selected .tldr file(s). """
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
        """ Method called when words are selected in the right list containing 
        words in the list that the teacher is building. """
        if self.view.center_list.model or self.view.right_list.model:
            selection = self.view.right_list.listbox.curselection()
            if selection:
                self.view.word_properties.display(
                    [ self.view.right_list.model.get_value_by_index(int(i))
                      for i in selection ]
                )
            self.refresh_transfer_strip()
        else:
            self.view.word_properties.display([])

    def on_add_button(self):
        """ Method called when the add button in the TransferStripWidget is
        clicked. """
        selection = self.view.center_list.listbox.curselection()
        for index in selection:
            key = self.view.center_list.model.get_key_by_index(int(index))
            word = self.view.center_list.model[key]
            self.view.right_list.model[key] = word
        self.refresh_transfer_strip()

    def on_add_all_button(self):
        """ Method called when the add all button in the TransferStripWidget is 
        clicked. """
        for k, v in self.view.center_list.model.iteritems():
            self.view.right_list.model[k] = v
        self.refresh_transfer_strip()

    def on_remove_button(self):
        """ Method called when the remove button in the TransferStripWidget is
        clicked. """
        selection = self.view.right_list.listbox.curselection()
        for index in selection:
            key = self.view.right_list.model.get_key_by_index(int(index))
            del self.view.right_list.model[key]
        self.refresh_transfer_strip()
        self.on_center_list_select()

    def on_remove_all_button(self):
        """ Method called when the remove all button in the TransferStripWidget 
        is clicked. """
        self.view.right_list.model.clear()
        self.refresh_transfer_strip()
        self.on_center_list_select()

    def on_speak_button(self):
        """ Method called when the play button is pressed. """
        self.tts.panic()
        self.tts.speak(". ".join(word.word
                                for word in self.view.word_properties.model))

    def on_panic_button(self):
        """ Method called when the stop button is pressed. """
        self.tts.panic()

    def on_return_button(self):
        master = self.view.master
        self.view.destroy()
        t = teacher.TeacherInterface(master)
        t.pack()
        
        

    def on_import_button(self):
        """ Method called when the import button in the toolbar is pressed. """
        filenames = tkFileDialog.askopenfilenames(filetypes=[("Word List", ".tldr")])

        for filename in filenames:
            try:
                with open(filename, "r") as f:
                    list_Id = database.add_list(filename)
                    data = list(parse_tldr(f))  
                    for word in data:
                        try:
                            word_Id = database.add_word(word.word,
                                                        word.definition,
                                                        word.example,
                                                        word.difficulty)
                        except Exception:
                            pass
                        else:
                            database.add_wordlist_mappings(list_Id, word_Id)
            except IOError as e:
                tkMessageBox.showwarning(
                    "Import Error",
                    "Could not open {0}".format(filename)
                )
                logging.warn(e)  
            else:
                self.view.left_list.model[os.path.relpath(filename)] = data

    def on_create_button(self):
        """ Method called when the create new word button in the toolbar is
        pressed. """
        word = new_word_prompt()
        if word is not None:
            try:
                word_Id = database.add_word(word.word,
                                            word.definition,
                                            word.example,
                                            word.difficulty)
            except Exception:
                pass
            else:
                database.add_wordlist_mappings(1, word_Id)
        self.populate()
        self.on_left_list_select()

    def on_random_button(self):
        """ Method called when the create random list button in the
        TransferStripWidget is pressed. """ 
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
        """ Method called when the export button in the toolbar is pressed. """
        filename = tkFileDialog.asksaveasfilename(filetypes=[("Word List", ".tldr")])
        if not filename: return

        try:
            with open(filename, "w") as f:
                words = sorted(list(self.view.right_list.model.values()),
                               key=lambda x: x.word.lower())

                f.write("# Autogenerated by Spellorama Teacher Interface\n")
                f.write("# {0}\n".format(datetime.datetime.now().isoformat()))
                f.write("# {0} words\n".format(len(words)))
                for line in gen_tldr(words):
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
        

        lid = database.add_list(filename)
        for w in words:
            wid = database.get_word_id(w.word, w.definition, w.example, w.difficulty).fetchone()[0]
            database.add_wordlist_mappings(lid, wid)
        self.populate()

    def populate(self):
        """ Populates the list of lists with the files that are in the 
        database. """
        list_of_files = database.get_filenames()
        for list_ID,filename in list_of_files:
            words_in_file = database.get_words_from_file(list_ID)
            word_dict = {}
            for i in words_in_file:
                w = Word(i[1], i[2], i[3], i[4])
                word_dict[i[1]] = w
            self.view.left_list.model[filename] = word_dict

    def refresh_transfer_strip(self):
        """ Method called by all methods invoked when there are words added 
        to or removed from the list being built. Includes tests to see if the 
        buttons in the TransferStripWidget should be active or not. """
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
        """ Bind behaviours to views.py. """
        self.view = view

        view.left_list.listbox.bind("<<ListboxSelect>>",
                                    lambda _: self.on_left_list_select())

        view.center_list.listbox.bind("<<ListboxSelect>>",
                                      lambda _: self.on_center_list_select())

        view.right_list.listbox.bind("<<ListboxSelect>>",
                                     lambda _: self.on_right_list_select())

        view.toolkit.return_button['command'] = self.on_return_button
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
