from Tkinter import *

import database
import teacher

class StudentInterface(Frame):

    def __init__(self, master, student):
        self.master = master
        self.student = student        
        Frame.__init__(self, self.master)
        self.create_widgets()
    
    def create_widgets(self):
        self.welcome = Label(self, text="Welcome back, %s" % self.student[1])
        self.welcome.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.highscores_button = Button(self, text="High Scores",
                                        command=self.high_scores)
        self.highscores_button.grid(row=1, column=0, padx=5, pady=5)
        self.playgame_button = Button(self, text="Play the game", 
                                      command=self.play_game)
        self.playgame_button.grid(row=1, column=1, padx=5, pady=5)
        self.practice_button = Button(self, text="Practice", 
                                      command=self.practice)
        self.practice_button.grid(row=1, column=2, padx=5, pady=5)
        self.logout_button = Button(self, text="Log out", command=self.logout)
        self.logout_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    def logout(self):
        pass

    def practice(self):
        pass

    def play_game(self):
        self.destroy()
        pg = PlayGame(master=self.master, student=self.student)
        pg.pack()

    def high_scores(self):
        pass

class PlayGame(Frame):

    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, self.master)
        self.avail = database.get_available_lists(self.student[0])
        self.create_widgets()

    def create_widgets(self):
        self.l = Label(self, text="Your teacher has made the following lists " +
                                   "available to you.\n Select one and hit Start " 
                                   "to begin.")
        self.l.grid(row=0, column=0, padx=5, pady=5)
        self.lister = teacher.ScrollingListBox(master=self)
        self.lister.grid(row=1, column=0, padx=5, pady=5)
        self.start_button = Button(self, text="Start!", command=self.start)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)
        for l in self.avail:
            self.lister.listbox.insert(END, l[1])

    def start(self):
        pass

class Practice(Frame):
       
    def __init__(self, master, student):
        pass

    def create_widgets(self):
        pass

class HighScores(Frame):
    
    def __init__(self, master):
        pass

    def create_widgets(self):
        pass
	
