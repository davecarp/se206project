from Tkinter import *
import views
import controllers

class TeacherInterface(Frame):
    
    def __init__(self, master):
        self.master = master        
        Frame.__init__(self, self.master)
        self.create_widgets()

    def create_widgets(self):
        self.listeditor = Button(self, text="Edit Lists", 
                                 command=self.open_listeditor)
        self.listeditor.grid(row=0, column=0, padx=5, pady=5,)
        self.studentmanager = Button(self, text="Manage Students",
                                     command=self.open_studentmanager)
        self.studentmanager.grid(row=0, column=1, padx=5, pady=5)

    def open_listeditor(self):
        self.destroy()
        listEditor = views.ListEditorView(self.master)
        cont = controllers.ListEditorController(listEditor)
        listEditor.pack()
       
    def open_studentmanager(self):
        pass

