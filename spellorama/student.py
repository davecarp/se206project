from Tkinter import *

import database
import teacher
import operator
import game

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
        self.destroy()
        hs = HighScores(master=self.master, student=self.student)
        hs.pack()

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
        self.l.grid(row=0, columnspan=2, column=0, padx=5, pady=5)
        self.lister = teacher.ScrollingListBox(master=self)
        self.lister.grid(row=1, columnspan=2, column=0, padx=5, pady=5)
        self.cancel_button = Button(self, text="Return to main menu",
                                    command=self.cancel)
        self.cancel_button.grid(row=2, column=0, padx=5, pady=5)
        self.start_button = Button(self, text="Start!", command=self.start)
        self.start_button.grid(row=2, column=1, padx=5, pady=5)
        for l in self.avail:
            self.lister.listbox.insert(END, l[1])
        self.start_button['state'] = "disabled"
        self.lister.listbox.bind("<ButtonRelease-1>", self.list_selected)
        self.index = None

    def list_selected(self, event):
        self.start_button['state'] = "active"
        self.index = int(self.lister.listbox.curselection()[0])
        
    def cancel(self):
        self.destroy()
        s = StudentInterface(master=self.master, student=self.student)
        s.pack()

    def start(self):
        self.destroy()
        g = game.Game(self.master, self.student, self.avail[self.index])
        g.pack()

class Practice(Frame):
       
    def __init__(self, master, student):
        pass

    def create_widgets(self):
        pass

class HighScores(Frame):
    
    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, self.master)
        self.create_widgets()
        self.generate_scores(student=self.student)
        self.display_scores()

    def create_widgets(self):
        self.heading = Label(self, text='High Scores')
        self.heading.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.most_words_heading = Label(self, text='Most Words')
        self.most_words_heading.grid(row=1, column=0, padx=5, pady=5)
        self.most_words_first = Label(self)
        self.most_words_first.grid(row=1, column=1, padx=5, pady=5)
        self.most_words_second = Label(self)
        self.most_words_second.grid(row=2, column=1, padx=5, pady=5)
        self.most_words_third = Label(self)
        self.most_words_third.grid(row=3, column=1, padx=5, pady=5)
        self.correct_words_heading = Label(self, text="Most Correct Words")
        self.correct_words_heading.grid(row=4, column=0,
                                        padx=5, pady=5)
        self.correct_words_first = Label(self)
        self.correct_words_first.grid(row=4, column=1, padx=5, pady=5)
        self.correct_words_second = Label(self)
        self.correct_words_second.grid(row=5, column=1, padx=5, pady=5)
        self.correct_words_third = Label(self)  
        self.correct_words_third.grid(row=6, column=1, padx=5, pady=5)
        self.percent_correct_heading = Label(self, 
                                             text="Highest Percent Correct")
        self.percent_correct_heading.grid(row=7, column=0, padx=5, pady=5)
        self.percent_correct_first = Label(self)
        self.percent_correct_first.grid(row=7, column=1, padx=5, pady=5)
        self.percent_correct_second = Label(self)
        self.percent_correct_second.grid(row=8, column=1, padx=5, pady=5)
        self.percent_correct_third = Label(self)
        self.percent_correct_third.grid(row=9, column=1, padx=5, pady=5)
        self.you_most_words = Label(self, text="Your Rank") 
        self.you_most_words.grid(row=1, column=2, padx=5, pady=5)
        self.you_correct_words = Label(self, text="Your Rank")
        self.you_correct_words.grid(row=4, column=2, padx=5, pady=5)
        self.you_percent_correct = Label(self, text="Your Rank")
        self.you_percent_correct.grid(row=7, column=2, padx=5, pady=5)
        self.rank_most_words = Label(self)
        self.rank_correct_words = Label(self)
        self.rank_percent_correct = Label(self)
        self.rank_most_words.grid(row=2, rowspan=2, column=2, padx=5, pady=5)
        self.rank_correct_words.grid(row=5, rowspan=2, column=2, padx=5, pady=5)
        self.rank_percent_correct.grid(row=8, rowspan=2, column=2, padx=5, 
                                       pady=5)     
        self.return_button = Button(self, text="Return to Main",
                                    command=self.main)
        self.return_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)        
        
    def main(self):
        pass

    def generate_scores(self, student):
        self.student_list = database.get_student_list()
        self.by_words_spelt = sorted(self.student_list, 
                                     key=operator.itemgetter(5))
        self.by_words_correct = sorted(self.student_list, 
                                       key=operator.itemgetter(6))
        self.by_percent_correct = sorted(self.student_list,
                                         key=operator.itemgetter(8))
        for l in ([self.by_words_spelt, self.by_words_correct,
                   self.by_percent_correct]):
            l.reverse()
        self.student_ratings = [(self.by_words_spelt.index(student)+1),
                                (self.by_words_correct.index(student)+1),
                                (self.by_percent_correct.index(student)+1)]
        
        
    def display_scores(self):
        self.most_words_first['text'] = "1st: %s %d Words" % (self.by_words_spelt[0][1],
                                                              self.by_words_spelt[0][5])
        self.most_words_second['text'] = "2nd: %s %d Words" % (self.by_words_spelt[1][1],
                                                               self.by_words_spelt[1][5])
        self.most_words_third['text'] = "3rd: %s %d Words" % (self.by_words_spelt[2][1],
                                                              self.by_words_spelt[2][5])	
        self.correct_words_first['text'] = "1st: %s %d Words" % (self.by_words_correct[0][1],
                                                                 self.by_words_correct[0][6])
        self.correct_words_second['text'] = "2nd: %s %d Words" % (self.by_words_correct[1][1],
                                                                  self.by_words_correct[1][6])
        self.correct_words_third['text'] = "3rd: %s %d Words" % (self.by_words_correct[2][1],
                                                                 self.by_words_correct[2][6])
        self.percent_correct_first['text'] = "1st: %s %f%%" % (self.by_percent_correct[0][1],
                                                               self.by_percent_correct[0][8])
        self.percent_correct_second['text'] = "2nd: %s %f%%" % (self.by_percent_correct[1][1],
                                                                self.by_percent_correct[1][8])
        self.percent_correct_third['text'] = "3rd: %s %f%%" % (self.by_percent_correct[2][1],
                                                               self.by_percent_correct[2][8])
        self.rank_most_words['text'] = str(self.student_ratings[0])
        self.rank_correct_words['text'] = str(self.student_ratings[1])
        self.rank_percent_correct['text'] = str(self.student_ratings[2])



