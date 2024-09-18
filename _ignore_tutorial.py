# from myFilters import *

import tkinter as tk
from tkinter import messagebox


class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1080x720")
        self.root.title("Main window")

        # Menu bar
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_close)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="Hello From Main", font=("Outfit", 22))
        self.label.pack(pady=20, padx=30)

        self.txtbox = tk.Text(self.root, height=5, font=("Cairo", 16))
        self.txtbox.bind("<KeyPress>", self.shortcut)
        self.txtbox.pack(pady=20, padx=30)

        self.checkstate = tk.IntVar()

        self.checkbox = tk.Checkbutton(
            self.root,
            text="Show message!",
            font=("Cairo", 14),
            variable=self.checkstate,
        )
        self.checkbox.pack(padx=10, pady=10)

        self.button = tk.Button(
            self.root, text="Show Message", font=("Arial", 16), command=self.showMessage
        )
        self.button.pack(padx=10, pady=10)

        # self.labelt = tk.Label(self.root, text="checked")
        # self.labelf = tk.Label(self.root, text="not checked")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def showMessage(self):
        if self.checkstate.get() == 0:
            print(self.txtbox.get("1.0", tk.END)[:-1])
        else:
            messagebox.showinfo(title="Message", message=self.txtbox.get("1.0", tk.END))

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.showMessage()

    def on_close(self):
        if messagebox.askyesno(
            title="Confirm Quitting?", message="Are you sure you want to quit?"
        ):
            print("Oh you want to close?.. Fine..")
            self.root.destroy()


if __name__ == "__main__":
    Main()
