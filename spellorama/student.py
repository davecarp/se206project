from Tkinter import *

import database
import teacher
import operator
import game
import project
import os
import tkMessageBox

class StudentInterface(Frame):

    def __init__(self, master, student):
        self.master = master
        self.student = student        
        Frame.__init__(self, self.master, background="skyblue")
        self.initialise_pics()
        self.create_widgets()
    
    def initialise_pics(self):
        self.image_title = PhotoImage(file="pics/welcome_header.gif")
        self.image_highscores = PhotoImage(file="pics/viewhighscores.gif")
        self.image_game = PhotoImage(file="pics/playthegame.gif")
        self.image_practice = PhotoImage(file="pics/practice.gif")
        self.image_logout = PhotoImage(file="pics/logout.gif")
        self.button_height = max([self.image_highscores.height(), self.image_game.height(), 
                                  self.image_practice.height(), self.image_logout.height()])

    def create_widgets(self):

        label_title = Label(self, image=self.image_title, background="skyblue")
        label_title.image = self.image_title
        label_title.grid(row=0, column=0, columnspan=3,padx=10)

        self.welcome = Label(self, text="Nice to see you again, %s" % self.student[1],
                             font=('Comic Sans MS', 35, 'normal'),
                             background="skyblue", foreground="Black")
        self.welcome.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.highscores_button = Button(self, image=self.image_highscores,
                                        command=self.high_scores, height=self.button_height+5,
                                        width=self.image_highscores.width()+5,
                                        background="orange", activebackground="white")
        self.highscores_button.grid(row=2, column=0, padx=5, pady=5)
        self.playgame_button = Button(self, image=self.image_game, 
                                      command=self.play_game, height=self.button_height+5,
                                      background="orange", activebackground="white",
                                      width=self.image_game.width()+5)
        self.playgame_button.grid(row=2, column=1, padx=5, pady=5)
        self.practice_button = Button(self, image=self.image_practice, 
                                      command=self.practice, height=self.button_height+5,
                                      background="orange", activebackground="white",
                                      width=self.image_practice.width()+5)
        self.practice_button.grid(row=2, column=2, padx=5, pady=5)
        self.logout_button = Button(self, image=self.image_logout, command=self.logout,
                                    background="orange", activebackground="white",
                                    height=self.button_height+5,
                                    width=self.image_logout.width()+5)
        self.label = Label(self, text="'View High Scores' allows you to see "
                           "the best spellers in your class and how you "
                           "compare.\n 'Play the game' lets you spell lists "
                           "that your teacher has set for you.\n 'Practice' "
                           "lets you have another go at words you spelt "
                           "incorrectly in game mode", background="skyblue",
                           foreground="Black", font=('Comic Sans MS', 18, 'normal'))
        self.label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.logout_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    def logout(self):
        self.destroy()
        p = project.StartUpScreen(master = self.master)
        p.pack()

    def practice(self):
        self.destroy()
        p = Practice(master=self.master, student=self.student)
        p.pack()

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
        Frame.__init__(self, self.master, background="skyblue")
        self.avail = database.get_available_lists(self.student[0])
        self.initialise_pics()
        self.create_widgets()

    def initialise_pics(self):
        self.image_title = PhotoImage(file="pics/selectalist_header.gif")
        self.image_cancel = PhotoImage(file="pics/cancel.gif")
        self.image_start = PhotoImage(file="pics/start.gif")
    def create_widgets(self):
        label_title = Label(self, image=self.image_title, background="skyblue")
        label_title.image = self.image_title
        label_title.grid(row=0, column=0, columnspan=2,padx=10)
        self.l = Label(self, text="Your teacher has made the \nfollowing lists " +
                                   "available to you.\n Select one and hit Start " 
                                   "to begin.", font=('Comic Sans MS', 20, 'normal'),
                                    background="skyblue", foreground="Black")
        self.l.grid(row=1, columnspan=2, column=0, padx=5, pady=5)
        self.lister = teacher.ScrollingListBox(master=self)
        self.lister.grid(row=2, columnspan=2, column=0, padx=5, pady=5)
        self.cancel_button = Button(self, image=self.image_cancel,
                                    command=self.cancel,
                                    background="orange", activebackground="white")
        self.cancel_button.image = self.image_cancel
        self.cancel_button.grid(row=3, column=0, padx=5, pady=5)
        self.start_button = Button(self, image=self.image_start, command=self.start,
                                   background="orange", activebackground="white")
        self.start_button.image = self.image_start
        self.start_button.grid(row=3, column=1, padx=5, pady=5)
        for l in self.avail:
            self.lister.listbox.insert(END, l[1])
        self.start_button['state'] = "disabled"
        self.lister.listbox.bind("<ButtonRelease-1>", self.list_selected)
        self.lister.listbox['font'] = font=('Comic Sans MS', 14, 'normal')
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

class HighScores(Frame):
    
    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, self.master, background="skyblue")
        self.create_widgets()
        self.generate_scores(student=self.student)
        self.display_scores()

    def create_widgets(self):
        self.image_title = PhotoImage(file="pics/highscores_header.gif")
        self.heading = Label(self, image=self.image_title, background="skyblue")
        self.heading.image = self.image_title
        self.heading.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.most_words_heading = Label(self, text='Most Words',
                                        background="skyblue", foreground="Black",
                                        font=('Comic Sans MS', 15, 'normal'))
        self.most_words_heading.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.most_words_first = Label(self,  background="skyblue", foreground="Black",
                                      font=('Comic Sans MS', 15, 'normal'))
        self.most_words_first.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.most_words_second = Label(self,  background="skyblue", foreground="Black",
                                       font=('Comic Sans MS', 15, 'normal'))
        self.most_words_second.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.most_words_third = Label(self,  background="skyblue", foreground="Black",
                                      font=('Comic Sans MS', 15, 'normal'))
        self.most_words_third.grid(row=3, column=1, padx=5, pady=5, sticky=W)
        self.correct_words_heading = Label(self, text="Most Correct Words",
                                           background="skyblue", foreground="Black",
                                           font=('Comic Sans MS', 15, 'normal'))
        self.correct_words_heading.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.correct_words_first = Label(self, background="skyblue", foreground="Black",
                                         font=('Comic Sans MS', 15, 'normal'))
        self.correct_words_first.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.correct_words_second = Label(self, background="skyblue", foreground="Black",
                                          font=('Comic Sans MS', 15, 'normal'))
        self.correct_words_second.grid(row=5, column=1, padx=5, pady=5, sticky=W)
        self.correct_words_third = Label(self, background="skyblue", foreground="Black",
                                         font=('Comic Sans MS', 15, 'normal'))  
        self.correct_words_third.grid(row=6, column=1, padx=5, pady=5, sticky=W)
        self.percent_correct_heading = Label(self, 
                                             text="Highest Percent Correct",
                                             background="skyblue", foreground="Black",
                                             font=('Comic Sans MS', 15, 'normal'))
        self.percent_correct_heading.grid(row=7, column=0, padx=5, pady=5, sticky=W)
        self.percent_correct_first = Label(self, background="skyblue", foreground="Black",
                                           font=('Comic Sans MS', 15, 'normal'))
        self.percent_correct_first.grid(row=7, column=1, padx=5, pady=5, sticky=W)
        self.percent_correct_second = Label(self, background="skyblue", foreground="Black",
                                            font=('Comic Sans MS', 15, 'normal'))
        self.percent_correct_second.grid(row=8, column=1, padx=5, pady=5, sticky=W)
        self.percent_correct_third = Label(self, background="skyblue", foreground="Black",
                                           font=('Comic Sans MS', 15, 'normal'))
        self.percent_correct_third.grid(row=9, column=1, padx=5, pady=5, sticky=W)
        self.you_most_words = Label(self, text="Your Rank",
                                    background="skyblue", foreground="Black",
                                    font=('Comic Sans MS', 15, 'normal')) 
        self.you_most_words.grid(row=1, column=2, padx=5, pady=5)
        self.you_correct_words = Label(self, text="Your Rank",
                                       background="skyblue", foreground="Black",
                                       font=('Comic Sans MS', 15, 'normal'))
        self.you_correct_words.grid(row=4, column=2, padx=5, pady=5)
        self.you_percent_correct = Label(self, text="Your Rank",
                                         background="skyblue", foreground="Black",
                                         font=('Comic Sans MS', 15, 'normal'))
        self.you_percent_correct.grid(row=7, column=2, padx=5, pady=5)
        self.rank_most_words = Label(self, background="Black", foreground="Yellow",
                                     font=('Comic Sans MS', 30, 'normal'),
                                     width=3)
        self.rank_correct_words = Label(self, background="Black", foreground="Yellow",
                                        font=('Comic Sans MS', 30, 'normal'),
                                        width=3)
        self.rank_percent_correct = Label(self, background="Black", foreground="Yellow",
                                          font=('Comic Sans MS', 30, 'normal'),
                                          width=3)
        self.rank_most_words.grid(row=2, rowspan=2, column=2, padx=5, pady=5)
        self.rank_correct_words.grid(row=5, rowspan=2, column=2, padx=5, pady=5)
        self.rank_percent_correct.grid(row=8, rowspan=2, column=2, padx=5, 
                                       pady=5)
        self.image_main = PhotoImage(file="pics/returntomain.gif")     
        self.return_button = Button(self, image=self.image_main,
                                    command=self.main,
                                    background="orange", activebackground="white",
                                    width=self.image_main.width()+10,
                                    height=self.image_main.height()+10)
        self.return_button.image = self.image_main
        self.return_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)        
        
    def main(self):
        self.destroy()
        s = StudentInterface(self.master, self.student)
        s.pack()

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
        self.student_ratings = [(self.by_words_spelt.index(self.student)+1),
                                (self.by_words_correct.index(self.student)+1),
                                (self.by_percent_correct.index(self.student)+1)]
        
        
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

class Practice(Frame):

    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, self.master, background="skyblue")
        self.words = database.get_incorrect_words(self.student[0])
        if self.words == [] or self.words == None:
            tkMessageBox.showinfo("No words to spell", "You have no previously "
                                  "mis-spelt words to practice. You will now "
                                  "be redirected to the main menu.")
            self.destroy()
            s = StudentInterface(self.master, self.student)
            s.pack()
            return
        self.initialise_pics()
        self.attempts = 0
        self.word_count = 0
        self.current_word = self.words[self.word_count]
        self.create_widgets()

    def initialise_pics(self):
        self.image_title = PhotoImage(file="pics/practicemode.gif")
        self.image_hearword = PhotoImage(file="pics/hearword.gif")
        self.image_hearex = PhotoImage(file="pics/hearexample.gif")
        self.image_hint1 = PhotoImage(file="pics/hint1.gif")
        self.image_hint2 = PhotoImage(file="pics/hint2.gif")
        self.image_submit = PhotoImage(file="pics/submit.gif")
        self.image_quit = PhotoImage(file="pics/returntomain.gif")
        self.width=max([self.image_hint1.width(), self.image_hint2.width(),
                        self.image_hearword.width(), self.image_hearex.width()])+5
        self.height=max([self.image_hearword.height(), self.image_hearex.height(),
                         self.image_hint1.height(), self.image_hint2.height()])+5,    
       
    def create_widgets(self):
        self.header = Label(self, image=self.image_title,
                            background="skyblue")
        self.header.image = self.image_title
        self.header.grid(row=0, column=0, columnspan=30, padx=5, pady=5, sticky=W+E)
        self.title = Label(self, text="Word #1 out of %s"%str(len(self.words)), 
                           font=('Comic Sans MS', 30, 'normal'),
                           background="skyblue", foreground="Black")
        self.title.grid(row=1, columnspan=30, column=0, padx=5, pady=5, sticky=W+E)
        self.word_button = Button(self, image=self.image_hearword, width=self.width,
                                  command=self.hear_word, height=self.height,
                                  background="orange", activebackground="white")
        self.word_button.image = self.image_hearword
        self.word_button.grid(row=2, column=0, padx=5)
        self.example_button = Button(self, image=self.image_hearex, width=self.width,
                                     command=self.hear_example, height = self.height,
                                     background="orange", activebackground="white")
        self.example_button.image = self.image_hearex
        self.example_button.grid(row=3, column=0, padx=5)
        self.word_entry = Entry(self, font=('Comic Sans MS', 30, 'normal'))
        self.word_entry.grid(row=2, rowspan=2, column=1, padx=5, pady=5)
        self.submit_button = Button(self, image=self.image_submit, command=self.submit,
                                    background="orange", activebackground="white")
        self.submit_button.image = self.image_submit
        self.submit_button.grid(row=4, column=1, padx=5, pady=5)
        self.meaning_label = Label(self, font=('Comic Sans MS', 13, 'normal'),
                                   text="Meaning: %s"%self.current_word[2],
                                   background="skyblue", foreground="black",
                                   wraplength=600)
        self.meaning_label.grid(row=5, column=0, columnspan=30, padx=5, pady=5)
        self.quit_button = Button(self, image=self.image_quit,
                                  background="orange", activebackground="white",
                                  command=self.quit)
        self.quit_button.image = self.image_quit
        self.quit_button.grid(row=6, column=0, columnspan=30, padx=5, pady=5)
        self.get_num_letters = Button(self, image=self.image_hint1,
                                      background="orange", activebackground="white",
                                      height=self.height, width=self.width,
                                      command=self.get_letters)
        self.get_num_letters.image = self.image_hint1
        self.get_num_letters.grid(row=2, column=3, padx=5)
        self.get_starting_letter = Button(self, image=self.image_hint2,
                                          background="orange", activebackground="white",
                                          width=self.width, height=self.height,
                                          command=self.get_starting)
        self.get_starting_letter.grid(row=3, column=3,padx=5)
        self.get_num_letters['state'] = "disabled"
        self.get_starting_letter['state'] = "disabled"

    def hear_word(self):
        word = self.current_word[1]
        os.system("echo %s | festival --tts" % (word))

    def hear_example(self):
        example = self.current_word[3]
        os.system("echo %s | festival --tts" % (example))

    def get_letters(self):
        number = str(len(self.current_word[1]))
        tkMessageBox.showinfo("Number of letters", "There are %s letters in "
                              "the word you are trying to spell"%(number,))
        
    def get_starting(self):
        starting = str(self.current_word[1][0])
        tkMessageBox.showinfo("Starting letter", "The word that you are "
                              "trying to spell begins with an '%s'"%(starting,))
       
    def submit(self):
        entered = self.word_entry.get()
        self.word_entry.delete(0, END)
        if self.current_word[1] == entered:
            tkMessageBox.showinfo("Word Correct", "Congratulations, you spelt "
                                  "the word correct. Get ready to move onto "
                                  "the next word.")
            if self.attempts == 0:
                database.remove_incorrect_word(self.student[0], self.current_word[0])
            self.word_count += 1
            if (self.word_count+1) > len(self.words):
                tkMessageBox.showinfo("Practice Mode Complete", "You have "
                                      "respelt all previously incorrect words. "
                                      "You will now be returned to the main menu.")
                self.destroy()
                s = StudentInterface(self.master, self.student)
                s.pack()
                
            else:
                self.current_word = self.words[self.word_count]
                self.title['text'] = "Word #%d" % (self.word_count +1)
                self.get_num_letters['state'] = "disabled"
                self.get_starting_letter['state'] = "disabled"
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                return
        self.attempts += 1
        if self.attempts == 1:
            tkMessageBox.showinfo("Word Incorrect", "You spelt the word "
                                  "incorrectly this time. Hint #1 is now "
                                  "available. Have another go.")
            self.get_num_letters['state'] = "active"
            return
        if self.attempts == 2:
            tkMessageBox.showinfo("Word Incorrect", "You spelt the word "
                                  "incorrectly this time. Both hints are now "
                                  "available. Have another go.")
            self.get_starting_letter['state'] = "active"
            return
        if self.attempts == 3:
            self.word_count += 1
            if (self.word_count+1) > len(self.words):
                tkMessageBox.showinfo("Practice Mode Complete", "You have "
                                      "respelt all previously incorrect words. "
                                      "You will now be returned to the main menu.")
                self.destroy()
                s = StudentInterface(self.master, self.student)
                s.pack()
            else:
                tkMessageBox.showinfo("Word Incorrect", "You spelt the word "
                                      "incorrectly and have used up all your "
                                      "attempts. The correct spelling of the "
                                      "word was '%s'. You will automatically "
                                      "be moved on to the next word."
                                      % self.current_word[1])
                self.current_word = self.words[self.word_count] 
                self.attempts = 0
                self.get_num_letters['state'] = "disabled"
                self.get_starting_letter['state'] = "disabled"
                self.title['text'] = "Word #%d" % (self.word_count +1)
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                return
            

    def finish_game(self):
        self.destroy()
        r = ResultsScreen(self.master, self.student, self.result)
        r.pack()


    def quit(self):
        self.destroy()
        s = StudentInterface(self.master, self.student)
        s.pack()



