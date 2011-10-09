from Tkinter import *
import tkMessageBox
import hasher
import database
import teacher
import student


class StartUpScreen(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, background="Black")        
        self.create_widgets()

    def create_widgets(self):
        self.title = Label(self, text="The DC Spelling Bee", foreground="Yellow",
                           font=('Comic Sans MS', 50, 'normal'), background="Black")
        self.title.grid(row=0, column=0, columnspan=2,padx=10)
        self.login = Button(self, text="Login", command=self.open_login_screen,
			                font=('Comic Sans MS', 25, 'normal'), background="Yellow",
                            activebackground="Orange")
        self.login.grid(row=1, column=0, padx=20, pady=20)
        self.register = Button(self, text="Register", font=('Comic Sans MS', 25, 'normal'),
                               command=self.open_register_screen, background="Yellow",
                               activebackground="Orange")
        self.register.grid(row=1, column=1, padx=20, pady=20)

    def teacher_interface(self):
        self.destroy()   
        view = ListEditorView(master=root)
        controller = ListEditorController(view)
      
    def open_login_screen(self):
        self.destroy()
        login = LoginScreen(master=root)
        login.pack()

    def open_register_screen(self):
        self.destroy()
        register = RegistrationScreen(master=root)
        register.pack()
    
class LoginScreen(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master, background="Yellow")
        self.create_widgets()

    def create_widgets(self):
        for i, label_text in enumerate(["Username", "Password"]):
            label = Label(self, text=label_text, font=('Comic Sans MS', 25, 'normal'),
                          background="Yellow")
            label.grid(row=i, column=0, padx=5, pady=5)
        self.username_entry = Entry(self, font=('Comic Sans MS', 25, 'normal'))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry = Entry(self, font=('Comic Sans MS', 25, 'normal'))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.password_entry['show'] = "*"
        self.login_button = Button(self, text="Login", command=self.login,
                                   font=('Comic Sans MS', 18, 'normal'),
                                   foreground="Yellow", background="Black",
                                   activebackground="Orange")
        self.login_button.grid(row=2,column=0, padx=5, pady=5)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel,
                                    font=('Comic Sans MS', 18, 'normal'),
                                    foreground="Yellow", background="Black",
                                    activebackground="Orange")
        self.cancel_button.grid(row=2, column=1, padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()    
        password = self.password_entry.get()
        if not database.username_exists(username):
            tkMessageBox.showwarning("Login Failure", "Login Failed.\nPassword "
                                     "or Username incorrect. Please try again")
            return
        if hasher.test_hash(password, database.get_hashedpw(username)[0][0]):
            self.destroy()
            if database.get_account_type(username) == "student":
                self.destroy()
		student_screen = student.StudentInterface(master=root,
							  student=database.get_student(username))
		student_screen.pack()
            else:
                self.destroy()
                teacher_screen = teacher.TeacherInterface(master=root)
                teacher_screen.pack()
                
        else:
            tkMessageBox.showwarning("Login Failure", "Login Failed.\nPassword "
                                     "or Username incorrect. Please try again")            


    def cancel(self):
        self.destroy()
        startup = StartUpScreen(master=root)
        startup.pack()

class RegistrationScreen(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master, background="Yellow")
        self.create_type_selects()
        self.create_inputs()

    def create_type_selects(self):
        self.check_frame = Frame(self, background="Yellow")
        self.check_frame.pack(side=TOP, expand=True)
        self.v = IntVar()
        self.student_rb = Radiobutton(self.check_frame, text="Student", 
                                      variable=self.v, value=1, height=1,
                                      font=('Comic Sans MS', 20, 'normal'),
                                      background="Yellow", foreground="Black",
                                      activebackground="Orange")
        self.student_rb.grid(row=0, column=0, padx=5, pady=5)
        self.teacher_rb = Radiobutton(self.check_frame, text="Teacher", 
                                     variable=self.v, value=2, height=1,
                                     font=('Comic Sans MS', 20, 'normal'),
                                     background="Yellow", foreground="Black",
                                     activebackground="Orange")
        self.teacher_rb.grid(row=0, column=1, padx=5, pady=5)
        self.teacher_rb.bind("<Button-1>", self.tpw)
        self.student_rb.bind("<Button-1>", self.spw)
        self.tpw_label = None
        self.tpw_entry = None
        

    def create_inputs(self):
        self.inputs_frame = Frame(self, background="Yellow")        
        self.inputs_frame.pack(side=BOTTOM)
        for i, label_text in enumerate(["Name", "Username", "Password",
                                        "Confirm Password"]):
            label = Label(self.inputs_frame, text=label_text, width=19,
                          font=('Comic Sans MS', 20, 'normal'),
                          background="Yellow", foreground="Black")
            label.grid(row=i, column=0, padx=5, pady=5)
        self.name_entry = Entry(self.inputs_frame, font=('Comic Sans MS', 20, 'normal'))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.username_entry = Entry(self.inputs_frame, font=('Comic Sans MS', 20, 'normal'))
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        self.password_entry = Entry(self.inputs_frame, font=('Comic Sans MS', 20, 'normal'))
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.password_entry['show'] = "*"
        self.confpw_entry = Entry(self.inputs_frame, font=('Comic Sans MS', 20, 'normal'))
        self.confpw_entry.grid(row=3, column=1, padx=5, pady=5)
        self.confpw_entry['show'] = "*"
        self.rego_button = Button(self.inputs_frame, text="Register", command=self.register,
                                  font=('Comic Sans MS', 16, 'normal'),
                                  background="Black", foreground="Yellow",
                                  activebackground="Orange")
        self.rego_button.grid(row=4, column=0, padx=5, pady=5)
        self.cancel_button = Button(self.inputs_frame, text="Cancel", command=self.cancel,
                                    font=('Comic Sans MS', 16, 'normal'),
                                    background="Black", foreground="Yellow",
                                    activebackground="Orange")
        self.cancel_button.grid(row=4, column=1, padx=5, pady=5)
        self.type_selected = False
        

    def tpw(self, e):
        self.tpw_label = Label(self.check_frame, text="Enter teacher password",
                               font=('Comic Sans MS', 20, 'normal'),
                               background="Yellow", foreground="Black")
        self.tpw_label.grid(row=1, column=0, padx=5, pady=5)
        self.tpw_entry = Entry(self.check_frame,font=('Comic Sans MS', 20, 'normal'))
        self.tpw_entry.grid(row=1, column=1, padx=5, pady=5)
        self.tpw_entry['show'] = "*"
        self.type_selected = "teacher"

    def spw(self, e):
        if self.tpw_entry != None:
            self.tpw_label.destroy()
            self.tpw_entry.destroy()
            self.tpw_label = None
            self.tpw_entry = None
        self.type_selected = "student"


    def register(self):
        if not self.type_selected:
            tkMessageBox.showwarning("Registration Failure", "Must select if creating a "
                                     "student or teacher account.")
            return	

        if (self.tpw_entry != None) and (self.tpw_entry.get() != "engineering"):
            tkMessageBox.showwarning("Registration Failure", "Must enter correct password "
                                     "to create teacher account.")
            return
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_conf = self.confpw_entry.get()
        for x in [name, username, password, password_conf]:
            if x == "":
                tkMessageBox.showwarning("Registration Failure", "Please complete all fields.")
                return
        if password != password_conf:
            # Pop up window saying that passwords do not match
            tkMessageBox.showwarning("Registration Failure", 
                                     "The passwords you have entered do not match. "
                                     "Ensure that your passwords are matching and try again.")
            return
        if self.type_selected == "student":
            account_type = "student"
        else:
            account_type = "teacher"
        if database.username_exists(username):
            tkMessageBox.showwarning("Registration Failure",
                                     "The username that you have selected already exists. "
                                     "Please choose a different username.")
            return
        else:
            database.create_user(name, username, account_type, hasher.create_hash(password))
            self.destroy()
            login = LoginScreen(master=root)
            login.pack()
            
    def cancel(self):
        self.destroy()
        startup = StartUpScreen(master=root)
        startup.pack()

if __name__ == "__main__":
    root = Tk() 
    startup = StartUpScreen(master=root)
    root.title("Spelling Bee")   
    startup.pack()
    root.mainloop()
