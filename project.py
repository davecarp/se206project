from Tkinter import *
import tkMessageBox
from spellorama.controllers import ListEditorController
from spellorama.views import ListEditorView

class StartUpScreen(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)        
        self.create_widgets()

    def create_widgets(self):
        self.login = Button(self, text="Login", command=self.open_login_screen)
        self.login.pack(side=LEFT)
        self.register = Button(self, text="Register", 
                               command=self.open_register_screen)
        self.register.pack(side=RIGHT)

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
        Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        for i, label_text in enumerate(["Username", "Password"]):
            label = Label(self, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)
        self.username_entry = Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry = Entry(self)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2,column=0, padx=5, pady=5)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()    
        password = self.password_entry.get()
        print "Username is %s -- Password is %s" % (username, password)

    def cancel(self):
        self.destroy()
        startup = StartUpScreen(master=root)
        startup.pack()

class RegistrationScreen(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        for i, label_text in enumerate(["Name", "Age", "Username", "Password",
                                        "Confirm Password"]):
            label = Label(self, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        ages = ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
                "15", "16"]
        self.var = StringVar(self)
        self.var.set(ages[0])
        self.age_select = apply(OptionMenu, (self, self.var) + tuple(ages))
        self.age_select.grid(row=1, column=1, padx=5, pady=5)        
        self.username_entry = Entry(self)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)
        self.password_entry = Entry(self)
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)
        self.password_entry['show'] = "*"
        self.confpw_entry = Entry(self)
        self.confpw_entry.grid(row=4, column=1, padx=5, pady=5)
        self.confpw_entry['show'] = "*"
        self.rego_button = Button(self, text="Register", command=self.register)
        self.rego_button.grid(row=5, column=0, padx=5, pady=5)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=5, column=1, padx=5, pady=5)

    def register(self):
        name = self.name_entry.get()
        age = int(self.var.get())
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_conf = self.confpw_entry.get()
        if password == password_conf:
            #Add functionality
            print "%s %d %s %s %s" % (name, age, username, password, password_conf)
        else:
            # Pop up window saying that passwords do not match
            tkMessageBox.showwarning("Registration Failure", 
                                     "The passwords you have entered do not match. "
                                     "Ensure that your passwords are matching and try again.")
            
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
