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
        else:
            pop_message("Please provide an extension!", "info")
            return


class Process(tk.Toplevel):

    def __init__(self, parent, img_path) -> None:
        super().__init__(parent)

        self.img_path = img_path.strip()
        self.original_image = Image.open(self.img_path).convert("RGB")

        self.frame = ttk.Frame(self)
        self.frame.pack()

        self.imageFrame = ttk.LabelFrame(self.frame, text="Image")
        self.imageFrame.grid(row=0, column=0, padx=30, pady=15)

        self.processed_image = None

        self.imageCanvas = tk.Canvas(self.imageFrame, width=500, height=500)
        self.imageCanvas.grid(row=0, column=0, padx=10, pady=10)
        self.display_image(self.original_image)

        self.secondFrame = ttk.Frame(self.frame)
        self.secondFrame.grid(row=0, column=1, padx=30, pady=15)

        self.dropFrame = ttk.LabelFrame(self.secondFrame, text="Select a filter")
        self.dropFrame.grid(row=0, column=1, padx=10, pady=10)

        self.filtersDrop = ttk.Combobox(
            self.dropFrame,
            values=[
                "Box Blur",
                "Gaussian Blur",
                "Unsharp Mask",
                "Kernel",
                "Rank Filter",
                "Mode Filter",
            ],
            state="readonly",
        )
        self.filtersDrop.bind("<<ComboboxSelected>>", self.update_ui)
        self.filtersDrop.grid(row=0, column=0, padx=10, pady=10)

        self.applyFrame = ttk.LabelFrame(self.secondFrame, text="Apply Filters")
        self.applyFrame.grid(row=1, column=1, padx=10, pady=10)

        self.filtersFrame = ttk.Frame(self.applyFrame)
        self.filtersFrame.grid(row=0, column=1, padx=10, pady=10)

        self.buttonsFrame = ttk.Frame(self.applyFrame)
        self.buttonsFrame.grid(row=1, column=1, padx=0, pady=0)

        self.applyButton = ttk.Button(
            self.buttonsFrame, text="Apply Fitler", command=self.apply_filter
        )
        self.applyButton.grid(row=2, column=1, padx=5, pady=5)

        self.resetButton = ttk.Button(
            self.buttonsFrame,
            text="Reset Filter",
            command=lambda: self.display_image(self.original_image),
        )
        self.resetButton.grid(row=3, column=1, padx=5, pady=5)

    def display_image(self, img: Image.Image):
        img = img.resize((500, 500))
        self.tkImage = ImageTk.PhotoImage(img)
        self.imageCanvas.create_image(250, 250, anchor="c", image=self.tkImage)

    def forget_widgets(func):
        def wrapper(self):
            for widget in self.filtersFrame.winfo_children():
                widget.destroy()
            func(self)

        return wrapper

    def update_ui(self, event):
        self.myOptions = {
            "Box Blur": self.add_blur,
            "Gaussian Blur": self.add_blur,
            "Unsharp Mask": self.add_unsharp,
            "Kernel": self.add_kernel,
            "Rank Filter": self.add_rank,
            "Mode Filter": self.add_mode,
        }
        self.filterSelect = self.filtersDrop.get()

        print(self.filterSelect)
        print(event)
        self.myOptions.get(self.filterSelect)()

    @forget_widgets
    def add_blur(self):
        self.sep_var = tk.BooleanVar()
        self.separate = ttk.Checkbutton(
            self.filtersFrame,
            text="Separate Dimensions",
            variable=self.sep_var,
            command=self.gaussian_dims,
        )
        self.separate.grid(row=1, column=2, padx=10, pady=10)

        self.sliderX = tk.Scale(
            self.filtersFrame, from_=0, to=100, orient=tk.HORIZONTAL
        )
        self.sliderX.set(50)

        self.sliderY = tk.Scale(
            self.filtersFrame, from_=0, to=100, orient=tk.HORIZONTAL
        )
        self.sliderY.set(100)

        self.blurSlider = tk.Scale(
            self.filtersFrame, from_=0, to=100, orient=tk.HORIZONTAL
        )
        self.blurSlider.set(10)

        self.gaussian_dims()

    def gaussian_dims(self):
        if self.sep_var.get():
            self.blurSlider.grid_forget()

            self.sliderX.grid(row=1, column=0, padx=10, pady=10)
            self.sliderY.grid(row=1, column=1, padx=10, pady=10)
        else:
            self.sliderX.grid_forget()
            self.sliderY.grid_forget()

            self.blurSlider.grid(row=1, column=1, padx=10, pady=10)

    @forget_widgets
    def add_unsharp(self):
        self.unsharp_radius = tk.Scale(
            self.filtersFrame, from_=0, to=100, orient=tk.HORIZONTAL
        )
        self.unsharp_radius.set(2)
        self.unsharp_radius.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Radius").grid(row=0, column=2)

        self.unsharp_percent = tk.Scale(
            self.filtersFrame, from_=0, to=1000, orient=tk.HORIZONTAL
        )
        self.unsharp_percent.set(150)
        self.unsharp_percent.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Percent").grid(row=1, column=2)

        self.unsharp_thres = tk.Scale(
            self.filtersFrame, from_=0, to=255, orient=tk.HORIZONTAL
        )
        self.unsharp_thres.set(3)
        self.unsharp_thres.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Threshold").grid(row=2, column=2)

    @forget_widgets
    def add_kernel(self):
        self.sizeFrame = ttk.LabelFrame(self.filtersFrame, text="Select Kernel Size:")
        self.sizeFrame.grid(row=0, column=1, padx=5, pady=5)
        self.kernelSize = ttk.Combobox(
            self.sizeFrame,
            values=["3x3", "5x5"],
            state="readonly",
        )
        self.kernelSize.current(0)
        self.kernelSize.bind("<<ComboboxSelected>>", self.update_kernel)
        self.kernelSize.grid(row=0, column=1, padx=5, pady=5)

        self.presetsFrame = ttk.LabelFrame(self.filtersFrame, text="Select Preset:")
        self.presetsFrame.grid(row=1, column=1, padx=5, pady=5)
        self.kernelPresets = ttk.Combobox(
            self.presetsFrame,
            values=[
                "Blur",
                "Contour",
                "Detail",
                "Enhance Edges",
                "Enhance Edges (More)",
                "Emboss",
                "Find Edges",
                "Sharpen",
                "Smooth",
                "Smooth (More)",
            ],
            state="readonly",
        )
        self.kernelPresets.bind("<<ComboboxSelected>>", self.apply_preset)
        self.kernelPresets.grid(row=0, column=0, padx=5, pady=5)

        self.validate_int = self.filtersFrame.register(self.validate_intgeter)

        self.gridFrame = ttk.Frame(self.filtersFrame)
        self.gridFrame.grid(row=2, column=1, padx=10, pady=10)
        self.kernel_entries = []
        self.update_kernel()

        self.kernelScale = tk.Scale(
            self.filtersFrame, from_=0, to=255, orient=tk.HORIZONTAL
        )
        self.kernelScale.grid(row=3, column=1, padx=10, pady=10)

        self.kernelOffset = tk.Scale(
            self.filtersFrame, from_=0, to=255, orient=tk.HORIZONTAL
        )
        self.kernelOffset.grid(row=4, column=1, padx=10, pady=10)

    def update_kernel(self, event=None):
        self.kernel_entries.clear()
        for widget in self.gridFrame.winfo_children():
            widget.destroy()

        self.k_size = int(self.kernelSize.get()[0])

        for i in range(1, self.k_size + 1):
            for j in range(self.k_size):
                entry = ttk.Entry(
                    self.gridFrame,
                    width=5,
                    validate="key",
                    validatecommand=(self.validate_int, "%P"),
                )
                entry.grid(row=i, column=j, padx=5, pady=2)
                self.kernel_entries.append(entry)

    def validate_intgeter(self, val):
        if val == "":
            return True

        try:
            float(val)
            return True
        except ValueError:
            return False

    def apply_preset(self, event):
        # fmt: off
        presets = {
            "Blur": [
                5, [
                    1, 1, 1, 1, 1,
                    1, 0, 0, 0, 1,
                    1, 0, 0, 0, 1,
                    1, 0, 0, 0, 1,
                    1, 1, 1, 1, 1,
                ], 16, 0
            ],
            "Contour": [
                    3, [
                        -1, -1, -1,
                        -1,  8, -1,
                        -1, -1, -1,
                    ], 1, 255
                ],
            "Detail": [
                    3, [
                        0,  -1,  0,
                        -1, 10, -1,
                        0,  -1,  0,
                    ], 6, 0
                ],
            "Enhance Edges": [
                    3, [
                        -1, -1, -1,
                        -1, 10, -1,
                        -1, -1, -1,
                    ], 2, 0
                ],
            "Enhance Edges (More)": [
                    3, [
                        -1, -1, -1,
                        -1,  9, -1,
                        -1, -1, -1,
                    ], 1, 0
                ],
            "Emboss": [
                    3, [
                        -1, 0, 0,
                        0,  1, 0,
                        0,  0, 0,
                    ], 1, 128
                ],
            "Find Edges": [
                    3, [
                        -1, -1, -1,
                        -1,  8, -1,
                        -1, -1, -1,
                    ], 1, 0
                ],
            "Sharpen": [
                    3, [
                        -2, -2, -2,
                        -2, 32, -2,
                        -2, -2, -2,
                    ], 16, 0
                ],
            "Smooth": [
                    3, [
                        1, 1, 1,
                        1, 5, 1,
                        1, 1, 1,
                    ], 13, 0
                ],
            "Smooth (More)": [
                    5, [
                        1, 1,  1, 1, 1,
                        1, 5,  5, 5, 1,
                        1, 5, 44, 5, 1,
                        1, 5,  5, 5, 1,
                        1, 1,  1, 1, 1,
                    ], 100, 0
                ],
        }
        # fmt: on
        selected = self.kernelPresets.get()
        values = presets.get(selected)

        i_map = {3: 0, 5: 1}
        self.kernelSize.current(i_map.get(values[0]))
        self.update_kernel()

        for i in range(len(values[1])):
            self.kernel_entries[i].delete(0, tk.END)
            self.kernel_entries[i].insert(0, values[1][i])

        self.kernelScale.set(values[2])
        self.kernelOffset.set(values[3])

    @forget_widgets
    def add_rank(self):
        self.rankDrop = ttk.Combobox(
            self.filtersFrame,
            values=["Min Filter", "Median Filter", "Max Filter"],
            state="readonly",
        )
        self.rankDrop.bind("<<ComboboxSelected>>", self.update_rank_presets)
        self.rankDrop.grid(row=0, column=1, padx=10, pady=10)

        self.rankSize = tk.Scale(
            self.filtersFrame,
            from_=3,
            to=50,
            orient=tk.HORIZONTAL,
            command=lambda value: self.rankRank.config(to=max(0, int(value) ** 2 - 1)),
            resolution=2,
        )
        self.rankSize.set(3)
        self.rankSize.grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.filtersFrame, text="Size").grid(row=1, column=2, padx=10, pady=10)

        self.rankRank = tk.Scale(
            self.filtersFrame,
            from_=0,
            to=self.rankSize.get() ** 2 - 1,
            orient=tk.HORIZONTAL,
        )
        self.rankRank.set(self.rankSize.get() ** 2 / 2)
        self.rankRank.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.filtersFrame, text="Rank").grid(row=2, column=2, padx=10, pady=10)

    def update_rank_presets(self, event):
        size = self.rankSize.get()
        presets = {
            "Min Filter": 0,
            "Median Filter": int(size**2 / 2),
            "Max Filter": int(size**2 - 1),
        }

        selected = self.rankDrop.get()
        self.rankRank.set(presets.get(selected))

    @forget_widgets
    def add_mode(self):
        self.modeSlider = tk.Scale(
            self.filtersFrame, from_=0, to=50, orient=tk.HORIZONTAL
        )
        self.modeSlider.set(3)
        self.modeSlider.grid(row=0, column=1, padx=10, pady=10)

    def apply_filter(self):
        self.myValues = {
            "Box Blur": self.fetch_slider,
            "Gaussian Blur": self.fetch_slider,
            "Unsharp Mask": self.fetch_slider,
            "Kernel": self.fetch_kernel,
            "Rank Filter": self.fetch_slider,
            "Mode Filter": self.fetch_slider,
        }

        self.processed_image = process_image(
            self.original_image,
            self.filterSelect,
            self.myValues.get(self.filterSelect)(),
        )

        self.display_image(self.processed_image)

    def fetch_slider(self):
        visible = []

        for widget in self.filtersFrame.winfo_children():
            if widget.winfo_viewable():
                if isinstance(widget, tk.Scale):
                    visible.append(int(widget.get()))
        print(visible)
        return visible

    def fetch_kernel(self):
        try:
            kernel = [float(entry.get()) for entry in self.kernel_entries]
        except ValueError:
            pop_message("Please insert the kernel values", type="error")
            return
        return [
            (self.k_size,) * 2,
            kernel,
            float(self.kernelScale.get()),
            float(self.kernelOffset.get()),
        ]


def pop_message(text, type="info"):
    messagebox.showinfo("Alert", text, icon=type)


if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    Main()
    # print(list(get_func_defaults(ImageFilter.Kernel).items()))
