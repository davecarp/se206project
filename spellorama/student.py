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
        Frame.__init__(self, self.master, background="Yellow")
        self.create_widgets()
    
    def create_widgets(self):
        self.welcome = Label(self, text="Welcome back, %s" % self.student[1],
                             font=('Comic Sans MS', 35, 'normal'),
                             background="Yellow", foreground="Black")
        self.welcome.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.highscores_button = Button(self, text="View High Scores",
                                        command=self.high_scores,
                                        font=('Comic Sans MS', 18, 'normal'),
                                        background="Black", foreground="Yellow",
                                        activebackground="Orange")
        self.highscores_button.grid(row=1, column=0, padx=5, pady=5)
        self.playgame_button = Button(self, text="Play the game", 
                                      command=self.play_game,
                                      font=('Comic Sans MS', 18, 'normal'),
                                      background="Black", foreground="Yellow",
                                      activebackground="Orange")
        self.playgame_button.grid(row=1, column=1, padx=5, pady=5)
        self.practice_button = Button(self, text="Practice", 
                                      command=self.practice,
                                      font=('Comic Sans MS', 18, 'normal'),
                                      background="Black", foreground="Yellow",
                                      activebackground="Orange")
        self.practice_button.grid(row=1, column=2, padx=5, pady=5)
        self.logout_button = Button(self, text="Log out", command=self.logout,
                                    font=('Comic Sans MS', 20, 'normal'),
                                    background="Black", foreground="Yellow",
                                    activebackground="Orange",
                                    width=20)
        self.label = Label(self, text="'View High Scores' allows you to see "
                           "the best spellers in your class and how you "
                           "compare.\n 'Play the game' lets you spell lists "
                           "that your teacher has set for you.\n 'Practice' "
                           "lets you have another go at words you spelt "
                           "incorrectly in game mode", background="Yellow",
                           foreground="Black", font=('Comic Sans MS', 18, 'normal'))
        self.label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.logout_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def logout(self):
        self.destroy()
        p = project.StartUpScreen(master = self.master)
        p.pack()

    def practice(self):
        self.destroy()
        p = Practice(self.master, self.student)
        p. pack()

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

class Practice(Frame):

    def __init__(self, master, student):
        self.master = master
        self.student = student
        Frame.__init__(self, self.master)
        self.create_widgets()
        self.words = database.get_incorrect_words(self.student[0])
        if self.words == [] or self.words == None:
            tkMessageBox.showinfo("No words to spell", "You have no previously "
                                  "mis-spelt words to practice. You will now "
                                  "be redirected to the main menu.")
            self.destroy()
            s = StudentInterface(self.master, self.student)
            s.pack()
        self.attempts = 0
        self.word_count = 0
        self.current_word = self.words[self.word_count]
        
    def create_widgets(self):
        self.title = Label(self, text="Word #1", 
                           font=('Comic Sans MS', 30, 'normal'))
        self.title.grid(row=0, columnspan=3, column=0, padx=5, pady=5)
        self.word_button = Button(self, text="Hear Word", width=12,
                                  font=('Comic Sans MS', 13, 'normal'),
                                  command=self.hear_word)
        self.word_button.grid(row=1, column=0, padx=5)
        self.example_button = Button(self, text="Hear Example", width=12,
                                     font=('Comic Sans MS', 13, 'normal'),
                                     command=self.hear_example)
        self.example_button.grid(row=2, column=0, padx=5)
        self.word_entry = Entry(self, font=('Comic Sans MS', 30, 'normal'))
        self.word_entry.grid(row=1, rowspan=2, column=1, padx=5, pady=5)
        self.submit_button = Button(self, text="Submit", command=self.submit,
                                    font=('Comic Sans MS', 13, 'normal'),
                                    width=15)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.meaning_label = Label(self, font=('Comic Sans MS', 13, 'normal'),
                                   text="Meanging: Blah Blah Blob of bro")
        self.meaning_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.quit_button = Button(self, text="Quit without saving",
                                  font=('Comic Sans MS', 13, 'normal'),
                                  command=self.quit)
        self.quit_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.get_num_letters = Button(self, text="Hint #1",
                                      font=('Comic Sans MS', 13, 'normal'),
                                      command=self.get_letters)
        self.get_num_letters.grid(row=1, column=3, padx=5)
        self.get_starting_letter = Button(self, text="Hint #2",
                                          font=('Comic Sans MS', 13, 'normal'),
                                          command=self.get_starting)
        self.get_starting_letter.grid(row=2, column=3,padx=5)
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
                return
        self.result.append(0)
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
                return
            

    def finish_game(self):
        self.destroy()
        r = ResultsScreen(self.master, self.student, self.result)
        r.pack()


    def quit(self):
        self.destroy()
        s = student.StudentInterface(self.master, self.student)
        s.pack()



