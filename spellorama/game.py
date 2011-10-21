from Tkinter import *
import student
import database
import os
import tkMessageBox

class Game(Frame):

    def __init__(self, master, student, ls):
        self.master = master
        self.student = student
        self.ls = ls
        self.words = database.get_words_from_file(ls[0])
        Frame.__init__(self, self.master, background="skyblue")
        self.attempts = 0
        self.word_count = 0
        self.current_word = self.words[self.word_count]
        self.result = []
        self.initialise_pics()
        self.create_widgets()

    def initialise_pics(self):
        self.image_title = PhotoImage(file="pics/SpellingBee_Black.gif")
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
        self.word_button = Button(self, image=self.image_hearword,
                                  background="orange", activebackground="white",
                                  height=self.height, width=self.width,
                                  command=self.hear_word)
        self.word_button.image = self.image_hearword
        self.word_button.grid(row=2, column=0, padx=5)
        self.example_button = Button(self, image=self.image_hearex,
                                     height=self.height, width=self.width,
                                     background="orange", activebackground="white",
                                     command=self.hear_example)
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
                                   background="skyblue", foreground="Black",
                                   wraplength=600)
        self.meaning_label.grid(row=5, column=0, columnspan=30, padx=5, pady=5)
        self.quit_button = Button(self, image=self.image_quit,
                                  background="orange", activebackground="white",
                                  command=self.quit)
        self.quit_button.image = self.image_quit
        self.quit_button.grid(row=6, column=0, columnspan=30, padx=5, pady=5)
        self.get_num_letters = Button(self, image=self.image_hint1,
                                      height=self.height, width=self.width,
                                      background="orange", activebackground="white",
                                      command=self.get_letters)
        self.get_num_letters.image = self.image_hint1
        self.get_num_letters.grid(row=2, column=3, padx=5)
        self.get_starting_letter = Button(self, image=self.image_hint2,
                                          height=self.height, width=self.width,
                                          background="orange", activebackground="white",
                                          command=self.get_starting)
        self.get_starting_letter.image = self.image_hint1
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
                self.result.append(1)
            self.word_count += 1
            if (self.word_count+1) > len(self.words):
                self.finish_game()
                return
            else:
                self.current_word = self.words[self.word_count]
                self.title['text'] = "Word #%d out of %s" % (self.word_count +1, str(len(self.words)))
                self.get_num_letters['state'] = "disabled"
                self.get_starting_letter['state'] = "disabled"
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                self.attempts = 0
                return
        self.attempts += 1
        if self.attempts == 1:
            tkMessageBox.showinfo("Word Incorrect", "You spelt the word "
                                  "incorrectly this time. Hint #1 is now "
                                  "available. Have another go.")
            self.get_num_letters['state'] = "active"
            self.result.append(0)
            database.add_incorrect_word(self.student[0], self.current_word[0])
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
                self.finish_game()
                return
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
                self.title['text'] = "Word #%d out of %s" % (self.word_count +1, str(len(self.words)))
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                return
            

    def finish_game(self):
        database.remove_available_list(self.ls[0], self.student[0])
        self.destroy()
        r = ResultsScreen(self.master, self.student, self.result)
        r.pack()


    def quit(self):
        self.destroy()
        s = student.StudentInterface(self.master, self.student)
        s.pack()

class ResultsScreen(Frame):

    def __init__(self, master, student, result):
        self.master = master
        self.student = student
        self.results = result
        Frame.__init__(self, self.master, background="Yellow")
        self.calculate_results()
        self.create_widgets()
        self.commit_results()

    def create_widgets(self):
        self.label_one = Label(self, text="Your Results",
                               font=('Comic Sans MS', 30, 'normal'),
                               background="Yellow", foreground="Black")
        self.label_one.pack(side=TOP)
        self.label_two = Label(self, text="Words Spelt: %d"%self.total_words,
                               font=('Comic Sans MS', 15, 'normal'),
                               background="Yellow", foreground="Black")
        self.label_two.pack(side=TOP)
        self.label_three = Label(self, 
                                 text="Words Correct: %d"%self.words_correct,
                                 font=('Comic Sans MS', 15, 'normal'),
                                 background="Yellow", foreground="Black")
        self.label_three.pack(side=TOP)
        self.label_four = Label(self,
                                text="Words Incorrect: %d"%self.words_incorrect,
                                font=('Comic Sans MS', 15, 'normal'),
                                background="Yellow", foreground="Black")
        self.label_four.pack(side=TOP)
        self.label_five = Label(self,
                                text="Percent Correct: %f%%"%self.percent_correct,
                                font=('Comic Sans MS', 15, 'normal'),
                                background="Yellow", foreground="Black")
        self.label_five.pack(side=TOP)
        self.label_six = Label(self,
                               text="Percent Incorrect: %f%%"%self.percent_incorrect,
                               font=('Comic Sans MS', 15, 'normal'),
                               background="Yellow", foreground="Black"
                               )
        self.label_six.pack(side=TOP)
        self.home_button = Button(self, text="Return to main", command=self.main,
                                  font=('Comic Sans MS', 13, 'normal'),
                                  background="Black", foreground="Yellow",
                                  activebackground="Orange")
        self.home_button.pack(side=TOP)

    def calculate_results(self):
        self.total_words = len(self.results)
        self.words_correct = self.results.count(1)
        self.words_incorrect = self.total_words - self.words_correct
        self.percent_correct = (self.words_correct/float(self.total_words))*100
        self.percent_incorrect = 100 - self.percent_correct

    def main(self):
        self.destroy()
        s = student.StudentInterface(self.master, self.student)
        s.pack()

    def commit_results(self):
        new_total = self.student[5]+self.total_words
        new_correct = self.student[6]+self.words_correct
        new_incorrect = self.student[7]+self.words_incorrect
        new_percentc = (new_correct/float(new_total))*100
        new_percenti = 100-new_percentc
        database.update_users_scores(new_total, new_correct, new_incorrect,
                                     new_percentc, new_percenti, self.student[0])
        self.student = database.update_student(self.student[0])


