from Tkinter import Tk, BOTH

from spellorama.controllers import ListEditorController
from spellorama.views import ListEditorView

if __name__ == '__main__':
    root = Tk()
    root.title("Teacher Interface")
    view = ListEditorView(master=root)
    controller = ListEditorController(view)
    view.pack(fill=BOTH, expand=True)
    root.mainloop()

