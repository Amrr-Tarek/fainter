from myFilters import *

import os
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, ttk
from webbrowser import open as br_open


class Main:

    def __init__(self):
        # Window
        self.root = tk.Tk()
        # self.root.geometry("1080x720")
        self.root.title("Fainter")

        # Applying Style
        self.style = ttk.Style(self.root)
        self.root.tk.call("source", "forest-light.tcl")
        self.root.tk.call("source", "forest-dark.tcl")
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")

        self.mode = tk.BooleanVar(value=True)  # 0: light, 1: dark
        self.theme = tk.StringVar(value="azure")

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

        # View Menu
        self.viewMenu = tk.Menu(self.menuBar, tearoff=0)
        self.viewMenu.add_cascade(label="Change Theme")
        self.viewMenu.add_separator()

        self.viewMenu.add_radiobutton(
            label="Azure",
            command=lambda: self.update_theme("azure"),
            value="azure",
            variable=self.theme,
        )
        self.viewMenu.add_radiobutton(
            label="Forest",
            command=lambda: self.update_theme("forest"),
            value="forest",
            variable=self.theme,
        )
        self.viewMenu.add_separator()
        self.viewMenu.add_checkbutton(
            label="Enable Dark Mode",
            command=self.toggle_dark_mode,
            variable=self.mode,
        )

        # Cascading
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.helpMenu, label="Help")
        self.menuBar.add_cascade(menu=self.viewMenu, label="View")
        self.root.config(menu=self.menuBar)

        self.start(None)

        self.root.mainloop()

    def start(self, old_path):
        self.path1 = old_path

        self.frame = ttk.Frame(self.root)
        self.frame.pack()

        # row 0
        self.header = ttk.Label(
            self.frame,
            text="Welcome to Fainter\nStart by Importing your image from the box down below",
            font=("Cairo", 22),
            justify="c",
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # row 1
        ttk.Label(
            self.frame,
            text="We are currently not supporting exporting images with Alpha channel",
            font=("Cairo", 18),
            justify="c",
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # row 2
        ttk.Label(
            self.frame,
            text="Supported Formats:\nbmp, ico, jpg, jpeg, png",
            font=("Cairo", 14),
            justify="c",
        ).grid(row=2, column=0, columnspan=3, padx=10, pady=30)

        # row 3
        self.dirLabel = ttk.Label(
            self.frame, text="Choose an image:", font=("Cairo", 18)
        )
        self.dirLabel.grid(row=3, column=0, padx=10, pady=10)

        self.dirEntry = ttk.Entry(self.frame, width=70)
        self.dirEntry.grid(row=3, column=1, padx=10, pady=10)

        # Adding the old path if it exists
        if self.path1:
            self.dirEntry.insert(0, self.path1)

        self.dirButton = ttk.Button(
            self.frame, text="Browse", command=self.pass_dir, style="Accent.TButton"
        )
        self.dirButton.grid(row=3, column=2, padx=10, pady=10)

        # row 4
        self.proceed = ttk.Button(
            self.frame,
            text="Proceed>>",
            command=self.open_image,
            style="Accent.TButton",
        )
        self.proceed.grid(row=4, column=2, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_dark_mode(self):
        modes = {True: "dark", False: "light"}
        theme_name = "azure" if self.theme.get() == "azure" else "forest"
        self.style.theme_use(f"{theme_name}-{modes[self.mode.get()]}")

    def update_theme(self, prefix):
        theme_mode = "dark" if self.mode.get() else "light"
        self.style.theme_use(f"{prefix}-{theme_mode}")

    def on_close(self):
        if messagebox.askyesno(title="Quit?", message="Are you sure you want to Quit?"):
            self.root.destroy()

    def pass_dir(self):
        file_path = browse_open()

        if file_path:
            self.dirEntry.delete(0, tk.END)
            self.dirEntry.insert(0, file_path)

    def open_image(self):
        file_path = self.dirEntry.get().strip()  # Absolute

        if check_path(file_path):
            self.frame.destroy()

            # CREATE A TOPLEVEL WINDOW (NEW WINDOW)
            Process(self, file_path)


class Process:

    def __init__(self, parent: Main, img_path: str) -> None:
        self.path = img_path
        self.parent = parent
        self.master = self.parent.root

        self.img_path = img_path.strip()
        self.original_image = Image.open(self.img_path).convert("RGB")

        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        self.imageFrame = ttk.LabelFrame(self.frame, text="Image")
        self.imageFrame.grid(row=0, column=0, padx=30, pady=15)

        self.buttonsFrame = ttk.Frame(self.imageFrame)
        self.buttonsFrame.grid(row=1)

        self.backButton = ttk.Button(
            self.buttonsFrame, text="Back", command=self.clear_widgets
        )
        self.backButton.grid(row=0, column=0, padx=5, pady=10)

        self.anotherButton = ttk.Button(
            self.buttonsFrame,
            text="Open Image",
            command=self.open_another,
            style="Accent.TButton",
        )
        self.anotherButton.grid(row=0, column=2, padx=5, pady=10)

        self.processed_image = None

        self.imageCanvas = tk.Canvas(self.imageFrame)
        self.imageCanvas.grid(row=0, column=0, padx=10, pady=10)
        self.display_image(self.original_image)

        self.secondFrame = ttk.Frame(self.frame)
        self.secondFrame.grid(row=0, column=1, padx=30, pady=15)

        self.dropFrame = ttk.LabelFrame(self.secondFrame, text="Select a filter")
        self.dropFrame.grid(row=0, column=0, padx=10, pady=10)

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
        self.applyFrame.grid(row=1, column=0, padx=10, pady=10)

        self.filtersFrame = ttk.Frame(self.applyFrame)
        self.filtersFrame.grid(row=0, column=1, padx=10, pady=10)
        self.validate_int = (self.filtersFrame.register(self.validate_integer), "%P")

        self.buttonsFrame = ttk.Frame(self.applyFrame)
        self.buttonsFrame.grid(row=1, column=1, padx=5, pady=5)

        self.applyButton = ttk.Button(
            self.buttonsFrame,
            text="Apply Fitler",
            command=self.apply_filter,
            style="Accent.TButton",
        )
        self.applyButton.grid(row=2, column=0, padx=2, pady=2)

        self.resetButton = ttk.Button(
            self.buttonsFrame,
            text="Reset Filter",
            command=lambda: self.display_image(self.original_image),
        )
        self.resetButton.grid(row=2, column=1, padx=2, pady=2)

        self.saveFrame = ttk.LabelFrame(self.secondFrame, text="Save Image As")
        self.saveFrame.columnconfigure(0, weight=1)
        self.saveFrame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.saveEntry = ttk.Entry(self.saveFrame)
        self.saveEntry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.saveAs = ttk.Button(
            self.saveFrame,
            text="Save As..",
            command=self.browse_save,
            style="Accent.TButton",
        )
        self.saveAs.grid(row=0, column=1, padx=3, sticky="ew")

    def clear_widgets(self):
        self.frame.destroy()

        self.parent.start(self.path)

    def display_image(self, img: Image.Image):
        min_res = (180, 180)
        max_res = (800, 800)

        width, height = self.size_thres(img.size, min_res, max_res)
        img = img.resize((width, height))

        self.tkImage = ImageTk.PhotoImage(img)

        self.imageCanvas.config(width=width, height=height)
        self.imageCanvas.create_image(
            width / 2, height / 2, anchor="c", image=self.tkImage
        )

    def open_another(self):
        file_path = browse_open()
        if not file_path:  # feels unnecessary
            return

        if check_path(file_path):
            self.original_image = Image.open(file_path).convert("RGB")
            self.display_image(self.original_image)

    def size_thres(self, size, minimum, maximum):
        if all(minimum[i] <= size[i] <= maximum[i] for i in range(2)):
            return size

        width, height = size

        # Maximum
        if any(size[i] > maximum[i] for i in range(2)):
            max_width, max_height = maximum
            scale_factor = min(max_width / width, max_height / height)

            new_size = tuple(round(dim * scale_factor) for dim in size)

            if any(new_size[i] < minimum[i] for i in range(2)):
                messagebox.showwarning("Bad Aspect ratio", "Image too wide or too thin")
                return maximum
            return new_size

        # Minimum
        elif any(size[i] < maximum[i] for i in range(2)):
            min_width, min_height = minimum
            scale_factor = max(min_width / width, min_height / height)

            new_size = tuple(round(dim * scale_factor) for dim in size)

            if any(new_size[i] > maximum[i] for i in range(2)):
                messagebox.showwarning("Bad Aspect ratio", "Image too wide or too thin")
                return minimum
            return new_size

    def forget_widgets(func):
        def wrapper(self: "Process"):
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
        self.separate.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.be3 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.blurSlider = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.be3, value),
        )
        self.blurSlider.set(10)
        self.rad_label = ttk.Label(
            self.filtersFrame, text="Radius", anchor="c", width=8
        )

        self.be1 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.sliderX = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.be1, value),
        )
        self.x_label = ttk.Label(
            self.filtersFrame, text="Radius X", anchor="c", width=8
        )

        self.be2 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.sliderY = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.be2, value),
        )
        self.y_label = ttk.Label(
            self.filtersFrame, text="Radius Y", anchor="c", width=8
        )

        self.gaussian_dims()

    def gaussian_dims(self):
        if self.sep_var.get():
            self.be3.grid_forget()
            self.blurSlider.grid_forget()
            self.rad_label.grid_forget()

            self.be1.grid(row=0, column=0)
            self.sliderX.set(self.blurSlider.get())
            self.sliderX.grid(row=0, column=1, padx=10, pady=10)
            self.x_label.grid(row=0, column=2, padx=5, pady=5)

            self.be2.grid(row=1, column=0)
            self.sliderY.set(self.blurSlider.get())
            self.sliderY.grid(row=1, column=1, padx=10, pady=10)
            self.y_label.grid(row=1, column=2, padx=5, pady=5)
        else:
            self.be1.grid_forget()
            self.be2.grid_forget()
            self.sliderX.grid_forget()
            self.sliderY.grid_forget()
            self.x_label.grid_forget()
            self.y_label.grid_forget()

            self.be3.grid(row=0, column=0)
            self.blurSlider.grid(row=0, column=1, padx=10, pady=10)
            self.rad_label.grid(row=0, column=2, padx=5, pady=5)

    @forget_widgets
    def add_unsharp(self):
        self.ue1 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.ue1.grid(row=0, column=0, padx=5, pady=5)

        self.unsharp_radius = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.ue1, value),
        )
        self.unsharp_radius.set(2)
        self.unsharp_radius.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Radius").grid(row=0, column=2)

        self.ue2 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.ue2.grid(row=1, column=0, padx=5, pady=5)

        self.unsharp_percent = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=1000,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.ue2, str_to_int(value)),
        )
        self.unsharp_percent.set(150)
        self.unsharp_percent.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Percent").grid(row=1, column=2)

        self.ue3 = ttk.Label(self.filtersFrame, width=8, anchor="c")
        self.ue3.grid(row=2, column=0, padx=5, pady=5)

        self.unsharp_thres = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.ue3, str_to_int(value)),
        )
        self.unsharp_thres.set(3)
        self.unsharp_thres.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Threshold").grid(row=2, column=2)

    @forget_widgets
    def add_kernel(self):
        self.sizeFrame = ttk.LabelFrame(self.filtersFrame, text="Select Kernel Size:")
        self.sizeFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.kernelSize = ttk.Combobox(
            self.sizeFrame,
            values=["3x3", "5x5"],
            state="readonly",
        )
        self.kernelSize.current(0)
        self.kernelSize.bind("<<ComboboxSelected>>", self.update_kernel)
        self.kernelSize.grid(row=0, column=1, padx=5, pady=5)

        self.presetsFrame = ttk.LabelFrame(self.filtersFrame, text="Select Preset:")
        self.presetsFrame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
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

        self.gridFrame = ttk.Frame(self.filtersFrame)
        self.gridFrame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.kernel_entries: list[tk.Entry] = []
        self.update_kernel()

        self.ke1 = ttk.Label(self.filtersFrame, width=6, anchor=tk.CENTER, text=0)
        self.ke1.grid(row=3, column=2)
        self.kernelScale = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.ke1, value),
        )
        self.kernelScale.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.filtersFrame, text="Scale").grid(row=3, column=0)

        self.ke2 = ttk.Label(self.filtersFrame, width=6, anchor=tk.CENTER, text=0)
        self.ke2.grid(row=4, column=2)
        self.kernelOffset = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.ke2, value),
        )
        self.kernelOffset.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.filtersFrame, text="Offset").grid(row=4, column=0)

        self.scaleDisableVar = tk.BooleanVar()
        self.scaleDisable = ttk.Checkbutton(
            self.filtersFrame, text="Disable Scale", variable=self.scaleDisableVar
        )
        self.scaleDisable.grid(row=5, column=0, columnspan=3, pady=10)

        self.scaleDisableVar.trace_add("write", self.toggle_scale)

    def toggle_scale(self, *args):
        state_map = {True: "disabled", False: "normal"}

        self.kernelScale.config(state=state_map[self.scaleDisableVar.get()])

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
                    validatecommand=self.validate_int,
                )
                entry.grid(row=i, column=j, padx=5, pady=2)
                self.kernel_entries.append(entry)

    def validate_integer(self, val):
        if val in {"", "-", "+"}:
            return True

        try:
            float(val)
            return True
        except ValueError:
            return False

    def apply_preset(self, event):
        selected = self.kernelPresets.get()
        values = kernel_presets.get(selected)

        i_map = {3: 0, 5: 1}
        self.kernelSize.current(i_map.get(values[0]))
        self.update_kernel()

        for i in range(len(values[1])):
            self.kernel_entries[i].delete(0, tk.END)
            self.kernel_entries[i].insert(0, values[1][i])

        self.scaleDisableVar.set(False)
        self.kernelScale.set(values[2])
        self.kernelOffset.set(values[3])

    @forget_widgets
    def add_rank(self):
        self.rankDropFrame = ttk.LabelFrame(self.filtersFrame, text="Select Preset:")
        self.rankDropFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.rankDrop = ttk.Combobox(
            self.rankDropFrame,
            values=["Min Filter", "Median Filter", "Max Filter"],
            state="readonly",
        )
        self.rankDrop.bind("<<ComboboxSelected>>", self.update_rank_presets)
        self.rankDrop.grid(row=0, column=0, padx=5, pady=5)

        self.re1 = ttk.Label(self.filtersFrame, width=4, anchor="c", text=3)
        self.re1.grid(row=1, column=2)
        self.rankSize = tk.Scale(
            self.filtersFrame,
            from_=3,
            to=50,
            orient=tk.HORIZONTAL,
            command=lambda value: (
                self.rankRank.config(to=max(0, str_to_int(value) ** 2 - 1)),
                self.rankRank.set(min(self.rankRank.get(), str_to_int(value) ** 2 - 1)),
                self.update_box(self.re1, str_to_int(value)),
            ),
            resolution=2,
        )
        self.rankSize.set(3)
        self.rankSize.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.filtersFrame, text="Size").grid(row=1, column=0, padx=5, pady=5)

        self.re2 = ttk.Label(self.filtersFrame, width=4, anchor="c")
        self.re2.grid(row=2, column=2)
        self.rankRank = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=self.rankSize.get() ** 2 - 1,
            orient=tk.HORIZONTAL,
            command=lambda value: self.update_box(self.re2, str_to_int(value)),
        )
        self.rankRank.set(self.rankSize.get() ** 2 / 2)
        self.rankRank.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(self.filtersFrame, text="Rank").grid(row=2, column=0, padx=5, pady=5)

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
        self.me1 = ttk.Label(self.filtersFrame, width=4, anchor="c")
        self.me1.grid(row=0, column=2)
        self.modeSlider = ttk.Scale(
            self.filtersFrame,
            from_=0,
            to=50,
            orient=tk.HORIZONTAL,
            comman=lambda value: self.update_box(self.me1, str_to_int(value)),
        )
        self.modeSlider.set(4)
        self.modeSlider.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.filtersFrame, text="Radius").grid(
            row=0, column=0, padx=2, pady=2
        )

    def apply_filter(self):
        self.myValues = {
            "Box Blur": self.fetch_blur,
            "Gaussian Blur": self.fetch_blur,
            "Unsharp Mask": self.fetch_unsharp,
            "Kernel": self.fetch_kernel,
            "Rank Filter": self.fetch_rank,
            "Mode Filter": self.fetch_mode,
        }

        self.processed_image = process_image(
            self.original_image,
            self.filterSelect,
            self.myValues.get(self.filterSelect)(),
        )
        self.display_image(self.processed_image)

    def fetch_blur(self):
        visible = []

        for widget in self.filtersFrame.winfo_children():
            if widget.winfo_viewable():
                if isinstance(widget, tk.Scale):
                    visible.append(round(widget.get(), 2))

        return visible

    def fetch_unsharp(self):
        return [
            round(self.unsharp_radius.get(), 2),
            int(self.unsharp_percent.get()),
            int(self.unsharp_thres.get()),
        ]

    def fetch_kernel(self):
        try:
            kernel = [float(entry.get()) for entry in self.kernel_entries]
        except ValueError:
            messagebox.showerror("Alert", "Please insert the kernel values")
            raise Exception("Missing Kernel Values")

        return [
            (self.k_size,) * 2,
            kernel,
            (
                round(self.kernelScale.get(), 2)
                if not self.scaleDisableVar.get()
                else None
            ),
            round(self.kernelOffset.get(), 2),
        ]

    def fetch_rank(self):
        size = self.rankSize.get()
        rank = self.rankRank.get()
        return list(map(round, [size, rank]))

    def fetch_mode(self):
        return [round(self.modeSlider.get())]

    def update_box(self, var: tk.Label, value=0):
        try:
            value = int(value)
            var.config(text=value)

        except ValueError:
            try:
                value = float(value)
                var.config(text=round(value, 2))
            except ValueError:
                return

    def browse_save(self) -> str:
        file_path = filedialog.asksaveasfilename(
            parent=self,
            # defaultextension=".png",
            filetypes=(
                ("*", "*.png;*.jpg;*.jpeg;*.ico;*.bmp"),
                ("PNG Image", "*.png"),
                ("JPG/JPEG Image", "*.jpg;*.jpeg"),
                ("ICON", "*.ico"),
                ("Bitmap Image", "*.bmp"),
                ("All Files", "*.*"),
            ),
            initialdir=cwd,  # change to os.path.expanduser("~") upon deployment
            title="Save image as..",
        )  # returns the path selected by user

        if file_path:
            self.saveEntry.delete(0, tk.END)
            self.saveEntry.insert(0, file_path)

    def save_image(self):
        # save image using the saveEntry path and error handling here
        pass


def browse_open():
    file_path = filedialog.askopenfilename(
        filetypes=(
            ("*", "*.png;*.jpg;*.jpeg;*.ico;*.bmp"),
            ("PNG Image", "*.png"),
            ("JPG/JPEG Image", "*.jpg;*.jpeg"),
            ("ICON", "*.ico"),
            ("Bitmap Image", "*.bmp"),
            ("All Files", "*.*"),
        ),
        initialdir=cwd,  # change to os.path.expanduser("~") upon deployment
        title="Choose an image..",
    )
    return file_path


def check_path(file_path):
    format = os.path.splitext(file_path)[-1][1:]

    if not file_path:
        messagebox.showinfo("Alert", "Please choose an image!")
        return

    if not format:
        messagebox.showinfo("Alert", "Please provide an extension!")
        return

    if not os.path.exists(file_path):
        messagebox.showwarning("File not found!", "Provided file doesn't exist!")
        return

    if format not in {"png"}:
        messagebox.showwarning("Alert", "Unsupported file extension!")
        return

    return True


def str_to_int(value):
    return round(float(value))


if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    Main()
