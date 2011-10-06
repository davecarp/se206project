from Tkinter import *
import views
import controllers
import database

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
        self.destroy()
        stdman = StudentManager(self.master)
        stdman.pack()

class StudentManager(Frame):

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)
        self.list_of_students = database.get_student_list()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="Students") 
        self.label.grid(row=0, column = 0, padx=5, pady=5)       
        self.listbox_frame = Frame(self)
        self.listbox_frame.grid(row=1, column=0, padx=5, pady=5)
        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)
        for s in self.list_of_students:
            self.listbox.insert(END, s)
        self.listbox.bind("<ButtonRelease-1>", self.student_selected)
        self.reset_password = Button(self, text="Reset Password", command=self.reset)
        self.reset_password.grid(row=2, column=0, padx=5, pady=5)
        self.records = StudentRecordsWidget(master=self)
        self.records.grid(row=0, rowspan=3, column=1, padx=5, pady=5)

    def student_selected(self, event):
        index = self.listbox.curselection()[0]
        self.record.update(self.listbox.get(index))

    def reset(self):
        print "Hey"

class StudentRecordsWidget(Frame):
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="No student selected.")
        self.label.pack()    

    def update(self, student):
        pass

if __name__ == "__main__":
    root = Tk()
    t = TeacherInterface(master=root)
    t.pack()
    root.mainloop()












