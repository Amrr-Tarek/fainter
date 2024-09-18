from myFilters import *

import os
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, ttk

from webbrowser import open as br_open


class Main:

    def __init__(self) -> None:
        # Window
        self.root = tk.Tk()
        self.root.geometry("1080x720")
        self.root.title("Fainter")

        """
        # Background Image
        self.bg_img = Image.open(rf"{os.path.dirname(__file__)}\angryimg.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relheight=1, relwidth=1)
        """

        # Menu Bar
        self.menuBar = tk.Menu(self.root)

        # File Menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open File")  # Add a command
        self.fileMenu.add_command(label="Close Project")  # Add a command
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit!", command=self.on_close)

        # Help Menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(
            label="Ask for help",
            command=lambda: br_open("https://github.com/Amrr-Tarek"),
        )

        # Cascading
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.helpMenu, label="Help")
        self.root.config(menu=self.menuBar)

        # row 0
        self.header = tk.Label(
            self.root,
            text="Welcome to Fainter\nStart by Importing your image from the box down below",
            font=("Cairo", 22),
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # row 1
        tk.Label(
            self.root,
            text="We are currently not supporting exporting images with Alpha channel",
            font=("Cairo", 18),
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # row 2
        tk.Label(
            self.root,
            text="Supported Formats:\nbmp, ico, jpg, jpeg, png",
            font=("Cairo", 14),
        ).grid(row=2, column=0, columnspan=3, padx=10, pady=30)

        # row 3
        self.dirLabel = tk.Label(self.root, text="Choose an image:", font=("Cairo", 18))
        self.dirLabel.grid(row=3, column=0, padx=10, pady=10)

        self.dirEntry = tk.Entry(self.root, width=70, font=("Arial", 9))
        self.dirEntry.grid(row=3, column=1, padx=10, pady=10)

        self.dirButton = tk.Button(
            self.root, text="Browse", command=self.browse, font=("Cairo", 14)
        )
        self.dirButton.grid(row=3, column=2, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        # if messagebox.askyesno(title="Quit?", message="Are you sure you want to Quit?"):
        #     self.root.destroy()
        self.root.destroy()

    def browse(self) -> str:
        file_path = filedialog.askopenfilename(
            filetypes=(
                ("PNG Image", "*.png"),
                ("JPG/JPEG Image", "*.jpg;*.jpeg"),
                ("ICON", "*.ico"),
                ("Bitmap Image", "*.bmp"),
                ("All Files", "*.*"),
            ),
            initialdir=cwd,
            title="Choose an image..",
        )

        if file_path:
            self.dirEntry.delete(0, tk.END)
            self.dirEntry.insert(0, file_path)
        print(self.dirEntry.get())


if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    Main()
