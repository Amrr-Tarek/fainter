from myFilters import *

import tkinter as tk
from tkinter import messagebox


class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1080x720")
        self.root.title("Main window")

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

        self.root.mainloop()

    def showMessage(self):
        if self.checkstate.get() == 0:
            print(self.txtbox.get("1.0", tk.END)[:-1])
        else:
            messagebox.showinfo(
                title="Message", message=self.txtbox.get("1.0", tk.END)
            )
            
    def shortcut(self, event):
        print(event)


if __name__ == "__main__":
    Main()
