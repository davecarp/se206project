from Tkinter import *
import tkMessageBox
import views
import controllers
import database
import hasher
import project

class TeacherInterface(Frame):
    """ This class specifies the creation of the main teacher interface
    and the methods that the buttons within it call. """
    
    def __init__(self, master):
        self.master = master        
        Frame.__init__(self, self.master, background="skyblue")
        self.initialise_pics()
        self.create_widgets()

    def initialise_pics(self):
        """ Initialises the images that will be used on the buttons in the interface. """
        self.image_title = PhotoImage(file="pics/welcome_header.gif")        
        self.image_logout = PhotoImage(file="pics/logout.gif")
        self.image_edit = PhotoImage(file="pics/editlists.gif")
        self.image_manage = PhotoImage(file="pics/managestudents.gif")
        self.width = max([self.image_edit.width(), self.image_manage.width()]) + 5
        self.height = max([self.image_edit.height(), self.image_manage.height()]) + 5
        

    def create_widgets(self):
        """ Creates the widgets in the interface and places them on the screen. """
        label_title = Label(self, image=self.image_title, background="skyblue")
        label_title.image = self.image_title
        label_title.grid(row=0, column=0, columnspan=2, padx=20, pady=25)
        self.listeditor = Button(self, image=self.image_edit,
                                 background="orange", activebackground="white", 
                                 command=self.open_listeditor, width = self.width,
                                 height=self.height)
        self.listeditor.grid(row=1, column=0, padx=20, pady=20)
        self.studentmanager = Button(self, image=self.image_manage,
                                     background="orange", activebackground="white",
                                     command=self.open_studentmanager,
                                     width=self.width, height=self.height)
        self.studentmanager.image = self.image_manage
        self.studentmanager.grid(row=1, column=1, padx=20, pady=20)
        self.logout_button = Button(self, image=self.image_logout, command=self.logout,
                                    background="orange", activebackground="white",
                                    width=self.image_logout.width()+10,
                                    height=self.image_logout.height()+10)
        self.logout_button.image = self.image_logout
        self.logout_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

    def open_listeditor(self):
        """ Opens the list editor screen. """
        self.destroy()
        listEditor = views.ListEditorView(self.master)
        cont = controllers.ListEditorController(listEditor)
        listEditor.pack()
       
    def open_studentmanager(self):
        """ Opens the student manager screen. """
        self.destroy()
        stdman = StudentManager(self.master)
        stdman.pack()

    def logout(self):
        """ Logs the teacher out. """
        self.destroy()
        p = project.StartUpScreen(master = self.master)
        p.pack()

class StudentManager(Frame):

    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master, background="skyblue")
        self.list_of_students = database.get_student_list()
        self.create_widgets()

    def create_widgets(self):
        self.image = PhotoImage(file="pics/manage_header.gif")
        self.header = Label(self, image=self.image,
                            background="skyblue")
        self.header.image = self.image
        self.header.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.label = Label(self, text="Students", font=("", 100), background="skyblue") 
        self.label.grid(row=1, column = 0, padx=5, pady=5)       
        self.lister = ScrollingListBox(self)
        self.lister.grid(row=2, rowspan=5, column=0, padx=5, pady=5)
        for s in self.list_of_students:
            self.lister.listbox.insert(END, s[1])
        self.lister.listbox.bind("<ButtonRelease-1>", self.student_selected)
        self.reset_password = Button(self, text="Reset Password", command=self.reset,
                                     background="orange", activebackground="white")
        self.reset_password.grid(row=7, column=0, padx=5, pady=5)
        self.records = StudentRecordsWidget(master=self)
        self.records.grid(row=1, rowspan=5, column=1, padx=5, pady=5)
        self.set_lists = Button(self, text="Assign Lists to Student",
                                command=self.assign_lists,
                                background="orange", activebackground="white")
        self.return_to_main = Button(self, text="Return to Teacher Menu",
                                     command=self.main_menu,
                                     background="orange", activebackground="white")
        self.return_to_main.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.lister.listbox.selection_set(0)
        self.index = 0
        self.set_lists.grid(row=7, column=1, padx=5, pady=5)
        self.records.update(self.list_of_students[0])

    def assign_lists(self):
        self.destroy()
        assigner = ListAssigner(master=self.master, student=self.list_of_students[self.index])   
        assigner.pack()


    def student_selected(self, event):
        self.index = int(self.lister.listbox.curselection()[0])
        self.records.update(self.list_of_students[self.index])

    def reset(self):
        userID = int(self.list_of_students[self.index][0])
        userName = self.list_of_students[self.index][1]
        re = PasswordReset(userID, userName)
    
    def main_menu(self):
        self.destroy()
        t = TeacherInterface(master = self.master)
        t.pack()

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
        
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master, width=100, background="skyblue")
        self.create_widgets()

    def create_widgets(self):
        self.name_label = Label(self, text="No student selected.", background="skyblue")
        self.name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)    
        self.wordsspelt_label = Label(self, background="skyblue")
        self.wordsspelt_label.grid(row=1, column=0, padx=5, pady=5)
        self.wordsspelt_value = Label(self, background="skyblue")
        self.wordsspelt_value.grid(row=1, column=1, padx=5, pady=5)
        self.wordscorrect_label = Label(self, background="skyblue")
        self.wordscorrect_label.grid(row=2, column=0, padx=5, pady=5)
        self.wordscorrect_value = Label(self, background="skyblue")
        self.wordscorrect_value.grid(row=2, column=1, padx=5, pady=5)
        self.wordsincorrect_label = Label(self, background="skyblue")
        self.wordsincorrect_label.grid(row=3, column=0, padx=5, pady=5)
        self.wordsincorrect_value = Label(self, background="skyblue")
        self.wordsincorrect_value.grid(row=3, column=1, padx=5, pady=5)
        self.percentcorrect_label = Label(self, background="skyblue")
        self.percentcorrect_label.grid(row=4, column=0, padx=5, pady=5)
        self.percentcorrect_value = Label(self, background="skyblue")
        self.percentcorrect_value.grid(row=4, column=1, padx=5, pady=5)
        self.percentincorrect_label = Label(self, background="skyblue")
        self.percentincorrect_label.grid(row=5, column=0, padx=5, pady=5)
        self.percentincorrect_value = Label(self, background="skyblue")
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

class ListAssigner(Frame):
        
    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, master, background="skyblue")
        self.create_widgets()
        
    def create_widgets(self):
        self.title_label = Label(self, text="Assigning lists for %s" % (self.student[1]),
                                 background="skyblue", font=('Comic Sans MS', 20, 'normal'))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.all_label = Label(self, text="All Lists", background="skyblue",
                               font=('Comic Sans MS', 15, 'normal'))
        self.all_label.grid(row=1, column=0, padx=5, pady=5)
        self.avail_label = Label(self, text="Available Lists", background="skyblue",
                                 font=('Comic Sans MS', 15, 'normal'))
        self.avail_label.grid(row=1, column=2, padx=5, pady=5)
        self.all_lister = ScrollingListBox(self)
        self.all_lister.listbox.bind("<ButtonRelease-1>", self.list_selected)
        self.available_lister = ScrollingListBox(self)
        self.available_lister.listbox.bind("<ButtonRelease-1>", self.avail_list_selected)
        self.all_lister.grid(row=2, rowspan=4, column=0, padx=5,pady=5)
        self.available_lister.grid(row=2, rowspan=4, column=2,padx=5,pady=5)
        self.add_button = Button(self, text=">", width=2, command=self.add,
                                 background="orange", activebackground="white")
        self.add_button.grid(row=2, column=1, padx=5, pady=5)
        self.add_all_button = Button(self, text=">>", width=2, command=self.add_all,
                                     background="orange", activebackground="white")
        self.add_all_button.grid(row=3, column=1, padx=5, pady=5)
        self.remove_button = Button(self, text="<", width=2, command=self.remove,
                                    background="orange", activebackground="white")
        self.remove_button.grid(row=4, column=1, padx=5, pady=5)
        self.remove_all_button = Button(self, text="<<", width=2, command=self.remove_all,
                                        background="orange", activebackground="white")
        self.remove_all_button.grid(row=5, column=1, padx=5, pady=5)
        self.main_button = Button(self, text="Return to Student Manager", 
                                  command=self.main, background="orange", activebackground="white")
        self.main_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.populate_lists()
        for b in ([self.add_button, self.add_all_button, self.remove_button,
                   self.remove_all_button]):
            b['state'] = "disabled"
        self.list_index = None
        self.avail_index = None
        self.set_button_states()

    def set_button_states(self):
        if self.all:
            self.add_all_button['state']="normal"
        else:
            self.add_all_button['state']="disabled"
        if self.avail:
            self.remove_all_button['state']="normal"
        else:
            self.remove_all_button['state']="disabled"
        if self.list_index != None:
            self.add_button['state']="normal"
        else:
            self.add_button['state']="disabled"
        if self.avail_index != None:
            self.remove_button['state']="normal"
        else:
            self.remove_button['state']="disabled"


    def populate_lists(self):
        self.all = database.get_lists()
        self.all_names = []
        for l in self.all:
            self.all_names.append(l[1].split('/')[-1].split('.')[0])
        self.avail = database.get_available_lists(self.student[0])
        self.avail_names = []
        for l in self.avail:
            self.avail_names.append(l[1].split('/')[-1].split('.')[0])            
        for l in self.all_names:
            self.all_lister.listbox.insert(END, l)
        for l in self.avail_names:
            self.available_lister.listbox.insert(END, l)

    def list_selected(self, event):
        try:
            self.list_index = int(self.all_lister.listbox.curselection()[0])
        except Exception:
            pass
        self.set_button_states()

    def avail_list_selected(self, event):
        try:
            self.avail_index = int(self.available_lister.listbox.curselection()[0])
        except Exception:
            pass
        self.set_button_states()

    def add(self):
        list_to_add = self.all[self.list_index]
        if list_to_add not in self.avail:
            if list_to_add[1] == "Created Words":
                tkMessageBox.showwarning("Warning", "Cannot assign created "+
                                         "words list to student.")
                return
            else:
                self.avail.append(list_to_add)    
                self.available_lister.listbox.insert(END, list_to_add[1].split("/")[-1].split(".")[0])
                database.add_available_list(list_to_add[0], self.student[0])
        self.set_button_states()
    
    def add_all(self):
        for l in self.all:
            if l not in self.avail: 
                if l[1] == "Created Words":
                    tkMessageBox.showwarning("Warning", "Cannot assign created "+
                        "words list to student. All other lists were assigned.")
                else:
                    self.avail.append(l)    
                    self.available_lister.listbox.insert(END, l[1].split("/")[-1].split(".")[0])
                    database.add_available_list(l[0], self.student[0])
        self.set_button_states()

    def remove(self):
        list_to_remove = self.avail[self.avail_index]
        del self.avail[self.avail_index]
        self.available_lister.listbox.delete(self.avail_index)
        database.remove_available_list(list_to_remove[0], self.student[0])
        self.set_button_states()

    def remove_all(self):
        for l in self.avail:
            database.remove_available_list(l[0], self.student[0])
        self.avail = []
        self.available_lister.listbox.delete(0, END)
        self.set_button_states()

    def main(self):
        self.destroy()
        s = StudentManager(self.master)
        s.pack()

class ScrollingListBox(Frame):
        
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)

if __name__ == "__main__":
    root = Tk()
    t = TeacherInterface(master=root)
    t.pack()
    root.mainloop()












