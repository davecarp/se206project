from Tkinter import *
import tkMessageBox
import views
import controllers
import database
import hasher

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
            self.listbox.insert(END, s[1])
        self.listbox.bind("<ButtonRelease-1>", self.student_selected)
        self.reset_password = Button(self, text="Reset Password", command=self.reset)
        self.reset_password['state'] = "disabled"
        self.reset_password.grid(row=2, column=0, padx=5, pady=5)
        self.records = StudentRecordsWidget(master=self)
        self.records.grid(row=0, rowspan=3, column=1, padx=5, pady=5)

    def student_selected(self, event):
        self.reset_password['state'] = "active"
        self.index = int(self.listbox.curselection()[0])
        self.records.update(self.list_of_students[self.index])

    def reset(self):
        userID = int(self.list_of_students[self.index][0])
        userName = self.list_of_students[self.index][1]
        re = PasswordReset(userID, userName)

class PasswordReset(Toplevel):

    def __init__(self, userID, userName, master=None):
        Toplevel.__init__(self, master)
        self.title = "Reset Password"
        self.studentID = userID
        self.studentName = userName
        self.create_widgets()

    def create_widgets(self):
        self.toplabel = Label(self, text="Reset Password for %s" % (self.studentName))
        self.toplabel.grid(row=0, columnspan=2, column=0, padx=5, pady=5)
        self.pw_label = Label(self, text="Password")
        self.pw_label.grid(row=1, column=0, padx=5, pady=5)
        self.pw_entry = Entry(self)
        self.pw_entry.grid(row=1, column=1, padx=5, pady=5)
        self.pw_entry['show'] = "*"
        self.confpw_label = Label(self, text="Confirm Password")
        self.confpw_label.grid(row=2, column=0, padx=5, pady=5)
        self.confpw_entry = Entry(self)
        self.confpw_entry.grid(row=2, column=1, padx=5, pady=5)
        self.confpw_entry['show'] = "*"
        self.reset_button = Button(self, text="Reset Password", command=self.reset)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def reset(self):
        if self.pw_entry.get() != self.confpw_entry.get():
            tkMessageBox.showwarning("Reset Failed", "The passwords do not match."
                                     " Please re-enter matching passwords.")
        else:
            hashedpw = hasher.create_hash(self.pw_entry.get())
            database.change_password(self.studentID, hashedpw)
            self.destroy()

class StudentRecordsWidget(Frame):
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.name_label = Label(self, text="No student selected.")
        self.name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)    
        self.wordsspelt_label = Label(self)
        self.wordsspelt_label.grid(row=1, column=0, padx=5, pady=5)
        self.wordsspelt_value = Label(self)
        self.wordsspelt_value.grid(row=1, column=1, padx=5, pady=5)
        self.wordscorrect_label = Label(self)
        self.wordscorrect_label.grid(row=2, column=0, padx=5, pady=5)
        self.wordscorrect_value = Label(self)
        self.wordscorrect_value.grid(row=2, column=1, padx=5, pady=5)
        self.wordsincorrect_label = Label(self)
        self.wordsincorrect_label.grid(row=3, column=0, padx=5, pady=5)
        self.wordsincorrect_value = Label(self)
        self.wordsincorrect_value.grid(row=3, column=1, padx=5, pady=5)
        self.percentcorrect_label = Label(self)
        self.percentcorrect_label.grid(row=4, column=0, padx=5, pady=5)
        self.percentcorrect_value = Label(self)
        self.percentcorrect_value.grid(row=4, column=1, padx=5, pady=5)
        self.percentincorrect_label = Label(self)
        self.percentincorrect_label.grid(row=5, column=0, padx=5, pady=5)
        self.percentincorrect_value = Label(self)
        self.percentincorrect_value.grid(row=5, column=1, padx=5, pady=5)

    def update(self, student):
        self.name_label['text'] = student[1]
        self.wordsspelt_label['text'] = "Words Spelt:"
        self.wordscorrect_label['text'] = "Words Correct:"
        self.wordsincorrect_label['text'] = "Words Incorrect:"
        self.percentcorrect_label['text'] = "Percent Correct:"
        self.percentincorrect_label['text'] = "Percent Incorrect:"
        try:
            self.wordsspelt_value['text'] = "%d Words" % student[5]
        except TypeError:
            self.wordsspelt_value['text'] = "No Information Available"
        try:
            self.wordscorrect_value['text'] = "%d Words" % student[6]
        except TypeError:
            self.wordscorrect_value['text'] = "No Information Available"
        try:            
            self.wordsincorrect_value['text'] = "%d Words" % student[7]
        except TypeError:
            self.wordsincorrect_value['text'] = "No Information Available"
        try:
            self.percentcorrect_value['text'] = "%.2f %%" % student[8]
        except TypeError:
            self.percentcorrect_value['text'] = "No Information Available"
        try:
            self.percentincorrect_value['text'] = "%.2f %%" % student[9]
        except TypeError:
            self.percentincorrect_value['text'] = "No Information Available"
        self.completed_lists = Button(self, text='View Completed Lists', 
                                      command=self.view_lists)
        self.set_lists = Button(self, text="Assign Lists to Student",
                                command=self.assign_lists)
        self.completed_lists.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.set_lists.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def view_lists(self):
        pass

    def assign_lists(self):
        pass

if __name__ == "__main__":
    root = Tk()
    t = TeacherInterface(master=root)
    t.pack()
    root.mainloop()












