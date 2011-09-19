# http://effbot.org/tkinterbook/+
from Tkinter import *

class ListEditorView(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Teacher Interface")
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.toolkit_frame = Frame(self)
        self.toolkit_frame.pack(side=TOP)        
        self.list_frame = Frame(self)
        self.word_properties_frame = Frame(self)
        self.list_frame.pack(side=TOP)
        self.word_properties_frame.pack(side=BOTTOM)
        toolkit = ToolKit(self.toolkit_frame)
        toolkit.pack(side=TOP)
        a = ListViewer(self.list_frame)
        a.pack(side=LEFT)
        b = ListViewer(self.list_frame)
        b.pack(side=LEFT)
        self.buttons_frame = Frame(self.list_frame)
        self.buttons_frame.pack(side=LEFT)
        buttons = ["Add", "Add All", "Remove", "Remove All"]
        for button in buttons:
            button = Button(self.buttons_frame, text=button)
            button.pack(side=TOP)
            button['width'] = 10
            button['padx'] = 0

        c = ListViewer(self.list_frame)
        c.pack(side=LEFT)
        w = Label(self.word_properties_frame, text="WORD PROPERTIES GO HERE")
        w.pack()

class ListViewer(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.list_scrollbar = Scrollbar(self)
        self.list_scrollbar.pack(side=RIGHT, fill=Y)
        self.list_table = Listbox(self, yscrollcommand=self.list_scrollbar.set)
        self.list_table.pack(side=LEFT, fill=BOTH)
        self.list_scrollbar.config(command=self.list_table.yview)
        for x in range(1,101):
            self.list_table.insert(END, x)

class ToolKit(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        for x in ["Import List", "Create New Word", "Create Random List",
                  "Export List"]:
            x = Button(self, text=x)
            x.pack(side=LEFT)
            x['width'] = 18
        

root = Tk()
app = ListEditorView(master=root)
app.mainloop()
root.destroy()
        
        
