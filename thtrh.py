import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk, ImageFilter


def display_image(img):
    img = img.resize((500, 500), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)


import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk, ImageFilter


class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processor")

        self.original_image = None
        self.processed_image = None

        # UI Components
        self.upload_btn = tk.Button(
            master, text="Upload Image", command=self.upload_image
        )
        self.upload_btn.pack()

        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

        self.effect_var = tk.StringVar(value="Sharpen")
        self.effect_menu = tk.OptionMenu(master, self.effect_var, "Sharpen", "Blur")
        self.effect_menu.pack()

        # Slider for Sharpening
        self.sharpen_strength = tk.Scale(
            master, from_=1, to=10, label="Sharpening Strength", orient=tk.HORIZONTAL
        )
        self.sharpen_strength.set(5)
        self.sharpen_strength.pack()

        # Apply Button
        self.apply_btn = tk.Button(
            master, text="Apply Effect", command=self.apply_effect
        )
        self.apply_btn.pack()

        # Reset Button
        self.reset_btn = tk.Button(master, text="Reset Image", command=self.reset_image)
        self.reset_btn.pack()

        # Save Button
        self.save_btn = tk.Button(master, text="Save Image", command=self.save_image)
        self.save_btn.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)

    def apply_effect(self):
        if self.original_image is not None:
            effect = self.effect_var.get()
            if effect == "Sharpen":
                strength = self.sharpen_strength.get()
                kernel = ImageFilter.Kernel(
                    size=(3, 3),
                    kernel=[-1, -1, -1, -1, strength + 5, -1, -1, -1, -1],
                    scale=strength,
                    offset=0,
                )
                self.processed_image = self.original_image.filter(kernel)
            elif effect == "Blur":
                self.processed_image = self.original_image.filter(ImageFilter.BLUR)

            self.display_image(self.processed_image)

    def display_image(self, img):
        img = img.resize((500, 500), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def reset_image(self):
        if self.original_image is not None:
            self.display_image(self.original_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*"),
                ],
            )
            if file_path:
                self.processed_image.save(file_path)
                messagebox.showinfo(
                    "Image Saved", "Your image has been saved successfully!"
                )


# Run the application
root = tk.Tk()
app = ImageProcessorApp(root)
root.mainloop()
