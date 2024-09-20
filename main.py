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

        # Applying Style
        self.style = ttk.Style(self.root)
        self.root.tk.call("source", "forest-light.tcl")
        self.root.tk.call("source", "forest-dark.tcl")
        self.style.theme_use("forest-dark")

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

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # row 0
        self.header = tk.Label(
            self.frame,
            text="Welcome to Fainter\nStart by Importing your image from the box down below",
            font=("Cairo", 22),
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # row 1
        tk.Label(
            self.frame,
            text="We are currently not supporting exporting images with Alpha channel",
            font=("Cairo", 18),
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # row 2
        tk.Label(
            self.frame,
            text="Supported Formats:\nbmp, ico, jpg, jpeg, png",
            font=("Cairo", 14),
        ).grid(row=2, column=0, columnspan=3, padx=10, pady=30)

        # row 3
        self.dirLabel = tk.Label(
            self.frame, text="Choose an image:", font=("Cairo", 18)
        )
        self.dirLabel.grid(row=3, column=0, padx=10, pady=10)

        self.dirEntry = ttk.Entry(self.frame, width=70)
        self.dirEntry.grid(row=3, column=1, padx=10, pady=10)

        self.dirButton = ttk.Button(self.frame, text="Browse", command=self.browse_open)
        self.dirButton.grid(row=3, column=2, padx=10, pady=10)

        # row 4
        self.proceed = ttk.Button(
            self.frame,
            text="Proceed>>",
            command=self.open_image,
        )
        self.proceed.grid(row=4, column=2, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        # if messagebox.askyesno(title="Quit?", message="Are you sure you want to Quit?"):
        #     self.root.destroy()
        self.root.destroy()

    def browse_open(self):
        file_path = filedialog.askopenfilename(
            filetypes=(
                ("*", "*.png;*.jpg;*.jpeg;*.ico;*.bmp"),
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

    def open_image(self):
        file_path = self.dirEntry.get().strip()  # Absolute
        format = os.path.splitext(file_path)[-1][1:]
        # Process(self.root, file_path)
        # if not file_path:
        #     Process(self.root)
        #     return
        # else:
        #     Process(self.root, file_path)
        #     return

        if not file_path:
            pop_message("Please choose an image!", "info")
            return

        if format:
            if not os.path.exists(file_path):
                pop_message("Provided file doesn't exist!", "warning")
                return
            if format not in supported:
                pop_message("Unsupported file extension!", "warning")
                return
            # CREATE A TOPLEVEL WINDOW (NEW WINDOW)
            Process(self.root, file_path)
            process_image(file_path)
        else:
            pop_message("Please provide an extension!", "info")
            return


class Process(tk.Toplevel):

    def __init__(
        self,
        parent,
        img_path=r"D:\Courses\projects\fainter\medium.png",
    ) -> None:
        super().__init__(parent)

        img_path = img_path.strip()
        self.original_image = Image.open(img_path).convert("RGB")

        self.frame = ttk.Frame(self)
        self.frame.pack()

        self.imageFrame = ttk.LabelFrame(self.frame, text="Image")
        self.imageFrame.grid(row=0, column=0, padx=30, pady=15)

        self.processed_image = None

        self.imageCanvas = tk.Canvas(self.imageFrame, width=500, height=500)
        self.imageCanvas.grid(row=0, column=0, padx=10, pady=10)
        self.display_image(self.original_image)

        self.filtersFrame = ttk.LabelFrame(self.frame, text="Apply Filters")
        self.filtersFrame.grid(row=0, column=1, padx=10, pady=10)

        self.sliderControl = tk.Scale(
            self.filtersFrame, from_=0, to=100, orient=tk.HORIZONTAL
        )
        self.sliderControl.set(10)
        self.sliderControl.grid(row=0, column=1, padx=10, pady=10)

        self.applyButton = ttk.Button(
            self.filtersFrame, text="Apply Fitler", command=self.apply_filter
        )
        self.applyButton.grid(row=2, column=1, padx=5, pady=5)

        self.resetButton = ttk.Button(
            self.filtersFrame,
            text="Reset Filter",
            command=lambda: self.display_image(self.original_image),
        )
        self.resetButton.grid(row=3, column=1, padx=5, pady=5)

    def display_image(self, img: Image.Image):
        img = img.resize((500, 500))
        self.tkImage = ImageTk.PhotoImage(img)
        self.imageCanvas.create_image(250, 250, anchor="c", image=self.tkImage)

    def apply_filter(self):
        self.processed_image = process_image(
            self.original_image, self.sliderControl.get()
        )
        self.display_image(self.processed_image)


def pop_message(text, type="info"):
    messagebox.showinfo("Alert", text, icon=type)


if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    Main()
    # print(list(get_func_defaults(ImageFilter.Kernel).items()))
