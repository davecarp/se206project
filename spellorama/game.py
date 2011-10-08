from Tkinter import *
import student

class Game(Frame):

    def __init__(self, master, student, ls):
        self.master = master
        self.student = student
        self.ls = ls
        Frame.__init__(self, self.master)
        self.create_widgets()

    def create_widgets(self):
        l = Label(self, text="Game Window")
        l.pack()

