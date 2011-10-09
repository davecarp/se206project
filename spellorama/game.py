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
        Frame.__init__(self, self.master)
        self.attempts = 0
        self.word_count = 0
        self.current_word = self.words[self.word_count]
        self.result = []
        self.create_widgets()

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
                                   text="Meaning: %s"%self.current_word[2])
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
                self.result.append(1)
            self.word_count += 1
            if (self.word_count+1) > len(self.words):
                self.finish_game()
                return
            else:
                self.current_word = self.words[self.word_count]
                self.title['text'] = "Word #%d" % (self.word_count +1)
                self.get_num_letters['state'] = "disabled"
                self.get_starting_letter['state'] = "disabled"
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                return
        self.result.append(0)
        database.add_incorrect_word(self.student[0], self.current_word[0])
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
                self.title['text'] = "Word #%d" % (self.word_count +1)
                self.meaning_label['text'] = "Meaning: %s"%self.current_word[2]
                return
            

    def finish_game(self):
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
        Frame.__init__(self, self.master)
        self.calculate_results()
        self.create_widgets()
        self.commit_results()

    def create_widgets(self):
        self.label_one = Label(self, text="Your Results")
        self.label_one.pack(side=TOP)
        self.label_two = Label(self, text="Words Spelt: %d"%self.total_words)
        self.label_two.pack(side=TOP)
        self.label_three = Label(self, 
                                 text="Words Correct: %d"%self.words_correct)
        self.label_three.pack(side=TOP)
        self.label_four = Label(self,
                                text="Words Incorrect: %d"%self.words_incorrect)
        self.label_four.pack(side=TOP)
        self.label_five = Label(self,
                                text="Percent Correct: %f%%"%self.percent_correct)
        self.label_five.pack(side=TOP)
        self.label_six = Label(self,
                               text="Percent Incorrect: %f%%"%self.percent_incorrect)
        self.label_six.pack(side=TOP)
        self.home_button = Button(self, text="Return to main", command=self.main)
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


