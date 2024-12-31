import customtkinter as ctk
from customtkinter import filedialog
import os
from PIL import Image, ImageFilter, ImageTk
from CustomTkinterMessagebox import CTkMessagebox
from tkinter import ttk
import sv_ttk
from filters import *
from math import sqrt


class Main:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CTK test")
        # self.root.resizable(False, False)
        # self.root.geometry("580x275")
        
        ctk.set_appearance_mode("dark") # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue") # Themes: blue (default), dark blue, green
        sv_ttk.set_theme("dark")
        
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

        self.labelFrame = ctk.CTkLabel(
            self.frame,
            text="Welcome To Fainter\n\n Where you can easily preset your photos",
            font=("Cairo", 22),
            justify='c',
        ).grid(row=0, column=0, columnspan=3, padx=15, pady=20)
 
        self.secondLabel = ctk.CTkLabel(
            self.frame,
            text="supported Format (PNG, JPEG, ....)",
            font=("Arial", 16),
            justify='c'
        ).grid(row=1, column=0, columnspan=3, padx=15, pady=20)
        
        self.thirdLabel = ctk.CTkLabel(
            self.frame,
            text="Choose an image:",
            font=("Arial", 16),
            justify='c'
        ).grid(row=2, column=0, padx=15, pady=5)
        
        self.entry = ctk.CTkEntry(
            self.frame,
            width=300
        )
        self.entry.grid(row=2, column=1, padx=10, pady=5)

        self.browseButton = ctk.CTkButton(
            self.frame,
            text="Browse",
            command=self.set_dir,
            width=75,
        ).grid(row=2, column=2, padx=15, pady=5)

        self.proceedButton = ctk.CTkButton(
            self.frame,
            text="Proceed",
            command=self.open_img,
            width=75
        ).grid(row=3, column=2, padx=15, pady=15)
        
        self.root.mainloop()

    def set_dir(self):
        file_path = get_dir()

        if file_path:
            self.entry.delete(0, ctk.END)
            self.entry.insert(0, file_path)

    def open_img(self):
        file_path = self.entry.get().strip()

        if check_path(file_path):
            destroyer(self.frame)
            Process(self, file_path)
            

class Process:
    def __init__(self, parent: Main, file_path):
        self.root = parent.root
        path = file_path 
        
        self.img_path = path.strip()

        self.img = Image.open(self.img_path).convert("RGB")
        self.img_copy = self.img.copy()
        self.img = self.img.resize((500,500))

        img_ctk = ctk.CTkImage(light_image=self.img, dark_image=self.img, size=(400,400))

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()
        
        self.labelFrame = ttk.LabelFrame(self.frame, text="Image")
        self.labelFrame.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        
        self.photoLabel = ctk.CTkLabel(self.labelFrame, text="", image=img_ctk)
        self.photoLabel.grid(row=0, column=0, padx=10, pady=10)

        self.labelFrame2 = ttk.LabelFrame(self.frame, text="Filters")
        self.labelFrame2.grid(row=0, column=1,  padx=50, pady=5)
        values=[
                "Box Blur",
                "Gaussian Blur",
                "Unsharp Mask",
                "Kernel",
                "Rank Filter",
                "Mode Filter"
            ]
        self.comboBox = ctk.CTkComboBox(
            self.labelFrame2,
            values=values,
            state="readonly",
            command=lambda v: self.prepare_filter(v)
            )
        self.comboBox.grid(row=0, column=0, pady=20, padx=20)
        self.comboBox.set("Select preset")
        # self.comboBox.bind("<ComboBoxSelected>", command=lambda v: print(v))

    def prepare_filter(self, filter_name):
        self.filter_widget(filter_name)  

    def filter_widget(self, preset):
   
        if hasattr(self, "filterFrame") == False:
            self.filterFrame = ttk.Labelframe(self.frame, text='Custom')
            self.filterFrame.grid(row=1, column=1, padx=10, pady=10)

            self.buttonFrame = ctk.CTkFrame(self.filterFrame)
            self.buttonFrame.grid(row=2, column=0, columnspan=5, padx=30, pady=15)

            self.applyButton = ctk.CTkButton(self.buttonFrame, text="Apply", width=75)
            self.applyButton.grid(row=0, column=0, padx=10, pady=10)

            self.resetButton = ctk.CTkButton(self.buttonFrame,
                                            text="reset",
                                            width=75,
                                            fg_color="grey",
                                            command=self.reset_img)
            self.resetButton.grid(row=0, column=1, padx=10, pady=10)

        widget_dict = {
            "Box Blur": self.widget_boxBlur,
            "Kernel": self.widget_kernel,
            "Gaussian Blur": self.widget_gaussianBlur,
            "Unsharp Mask": self.widget_unsharpenMask,
            "Rank Filter": self.widget_rankFilter,
            "Mode Filter": self.widget_modeFitler
        }
        
        if hasattr(self, "lastFilter") == False or self.lastFilter != preset:
            if hasattr(self, "editFrame"):
                destroyer(self.editFrame)
            self.lastFilter = preset
            widget_dict.get(preset)()
        

    def widget_boxBlur(self):
        self.editFrame = ctk.CTkFrame(self.filterFrame)
        self.editFrame.grid(row=0, column=0, columnspan=5, padx=40, pady=20)

        self.scaleFrame = ctk.CTkFrame(self.editFrame)
        self.scaleFrame.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        self.scaleLabel1 = ctk.CTkLabel(self.scaleFrame, text="10.0", width=40)
        self.scaleLabel1.grid(row=0, column=0, padx=7)

        self.scaleLabel2 = ctk.CTkLabel(self.scaleFrame, text="Radius")
        self.scaleLabel2.grid(row=0, column=3, padx=7)

        self.applyButton.configure(
            command=lambda : self.apply_filter(self.lastFilter, float(self.scaleLabel1.cget("text")))
            )

        self.scale1 = ctk.CTkSlider(
            self.scaleFrame,
            from_=0, to=100,
            command= lambda v: self.scaleLabel1.configure(text=v),
            number_of_steps=200
            )
        self.scale1.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.scale1.set(10)

        self.checkBox = ctk.CTkCheckBox(
            self.editFrame,
            text="Separate dimensions",
            command=lambda: self.checkBox_checked(),
            ) 
        self.checkBox.grid(row=2, column=0, columnspan=5,pady=10)

        return

    def checkBox_checked(self):
        if self.checkBox.get() == 0:
            destroyer(self.scaleFrame1)
            self.scaleLabel2.configure(text="Radius")

        if self.checkBox.get() == 1:
            self.scaleLabel2.configure(text="Radius X")
            self.scaleFrame1 = ctk.CTkFrame(self.editFrame)
            self.scaleFrame1.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

            self.scaleLabel3 = ctk.CTkLabel(self.scaleFrame1, text="10.0", width=40)
            self.scaleLabel3.grid(row=1, column=0, padx=7)

            self.scaleLabel4 = ctk.CTkLabel(self.scaleFrame1, text="Radius Y")
            self.scaleLabel4.grid(row=1, column=3, padx=7)

            self.scale2 = ctk.CTkSlider(
            self.scaleFrame1,
            from_=0, to=100,
            command= lambda v: self.scaleLabel3.configure(text=v),
            number_of_steps=200
            )
            self.scale2.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

            self.scale2.set(10)
            self.scale1.set(10)
            self.scaleLabel1.configure(text="10.0")

            self.applyButton.configure(
            command=lambda : self.apply_filters((self.scaleLabel1.cget("text"),
                                                 self.scaleLabel3.cget("text"))
                                                 )
            )

    def widget_gaussianBlur(self):
        self.widget_boxBlur()
        print("alright")
        # self.applyButton.configure(command)
    def widget_unsharpenMask(self):
        self.editFrame = ctk.CTkFrame(self.filterFrame)
        self.editFrame.grid(row=0, column=0, columnspan=5, padx=40, pady=20)

        self.scaleFrame = ctk.CTkFrame(self.editFrame)
        self.scaleFrame.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        self.scaleLabel1 = ctk.CTkLabel(self.scaleFrame, text="0", width=40)
        self.scaleLabel1.grid(row=0, column=0, padx=7)

        self.scaleLabel2 = ctk.CTkLabel(self.scaleFrame, text="Radius")
        self.scaleLabel2.grid(row=0, column=3, padx=14)

        self.applyButton.configure(
            command=lambda : self.apply_filters(float(self.scaleLabel1.cget("text")))
            )

        self.scale1 = ctk.CTkSlider(
            self.scaleFrame,
            from_=0, to=100,
            command= lambda v: self.scaleLabel1.configure(text=int(v)),
            number_of_steps=200
            )
        self.scale1.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.scale1.set(0)

        self.scaleFrame1 = ctk.CTkFrame(self.editFrame)
        self.scaleFrame1.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        self.scaleLabel3 = ctk.CTkLabel(self.scaleFrame1, text="0", width=40)
        self.scaleLabel3.grid(row=1, column=0, padx=7)

        self.scaleLabel4 = ctk.CTkLabel(self.scaleFrame1, text="Percent")
        self.scaleLabel4.grid(row=1, column=3, padx=12)

        self.applyButton.configure(
            command=lambda : self.apply_filters(float(self.scaleLabel3.cget("text")))
            )

        self.scale2 = ctk.CTkSlider(
            self.scaleFrame1,
            from_=0, to=1000,
            command= lambda v: self.scaleLabel3.configure(text=int(v)),
            number_of_steps=1000
            )
        
        self.scale2.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.scale2.set(0)

        self.scaleFrame2 = ctk.CTkFrame(self.editFrame)
        self.scaleFrame2.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        self.scaleLabel5 = ctk.CTkLabel(self.scaleFrame2, text="0", width=40)
        self.scaleLabel5.grid(row=2, column=0, padx=7)

        self.scaleLabel6 = ctk.CTkLabel(self.scaleFrame2, text="Threshold")
        self.scaleLabel6.grid(row=2, column=3, padx=7)

        self.applyButton.configure(
            command=lambda : self.apply_filters(float(self.scaleLabel5.cget("text")))
            )

        self.scale3 = ctk.CTkSlider(
            self.scaleFrame2,
            from_=0, to=255,
            command= lambda v: self.scaleLabel5.configure(text=int(v)),
            number_of_steps=255
            )
        self.scale3.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.scale3.set(0)

    def widget_kernel(self):
        self.editFrame = ctk.CTkFrame(self.filterFrame, fg_color="#1C1C1C")
        self.editFrame.grid(row=0, column=0, columnspan=5, padx=40, pady=5)

        self.labelFrame1 = ttk.Labelframe(self.editFrame, text="Select Kernel Size",
                                           borderwidth=3
                                           )
        self.labelFrame1.grid(row=0, column=0, pady=7, padx=15)

        values = ["3x3", "5x5"]
        self.comboBox1 = ctk.CTkComboBox(
            self.labelFrame1,
            values=values,
            state="readonly",
            command=lambda v: self.apply_dim(int(v[0]))
            )
        self.comboBox1.grid(row=0, column=0)
        self.comboBox1.set(values[0])

        self.labelFrame2 = ttk.LabelFrame(self.editFrame, text="Select Preset", borderwidth=3)
        self.labelFrame2.grid(row=1, column=0, pady=20, padx=15)
        
        self.comboBox2 = ctk.CTkComboBox(
            self.labelFrame2,
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
            command=lambda v: self.update_preset(v))
        self.comboBox2.grid(row=1, column=0)
        self.bigFrame = ctk.CTkFrame(self.editFrame)
        self.bigFrame.grid(row=3, column=0, pady=15)

        self.scaleFrame1 = ctk.CTkFrame(self.bigFrame)
        self.scaleFrame1.grid(row=0, column=0, pady=15, padx=15)

        self.scaleLabel1 = ctk.CTkLabel(self.scaleFrame1, text="0", width=40)
        self.scaleLabel1.grid(row=0, column=0, padx=15)

        self.scaleLabel2 = ctk.CTkLabel(self.scaleFrame1, text="Scale")
        self.scaleLabel2.grid(row=0, column=2, padx=20)

        self.scale1 = ctk.CTkSlider(
            self.scaleFrame1,
            from_=0,
            to=255,
            number_of_steps=255,
            command=lambda v: self.scaleLabel1.configure(text=int(v))
            )
        self.scale1.grid(row=0, column=1, padx=10)
        self.scale1.set(0)

        self.scaleFrame2 = ctk.CTkFrame(self.bigFrame)
        self.scaleFrame2.grid(row=1, column=0, pady=10)

        self.scaleLabel3 = ctk.CTkLabel(self.scaleFrame2, text="0", width=40)
        self.scaleLabel3.grid(row=0, column=0, padx=15)

        self.scaleLabel4 = ctk.CTkLabel(self.scaleFrame2, text="Offset")
        self.scaleLabel4.grid(row=0, column=2, padx=15)

        self.scale2 = ctk.CTkSlider(
            self.scaleFrame2,
            from_=0,
            to=255,
            number_of_steps=255,
            command=lambda v: self.scaleLabel3.configure(text=int(v))
            )
        self.scale2.grid(row=0, column=1, padx=10)
        self.scale2.set(0)

        self.checkBox = ctk.CTkCheckBox(
            self.bigFrame,
            text="Disable Scale",
            command=lambda : self.checkBox2()
            )
        self.checkBox.grid(row=2, column=0, pady=20)

        self.entryFrame1 = ctk.CTkFrame(self.editFrame, fg_color="#1C1C1C")
        self.entryFrame1.grid(row=2, column=0)
        
        self.entries(3)
    def update_preset(self, preset):
        count = 0
        for i in self.entryFrame1.winfo_children():
            count += 1
        count = sqrt(count)
        dim = kernel_presets.get(preset)[0]
        if count != dim:
            self.destroy_entries()
            self.entries(dim)
            self.entry_insertion(preset)
        else:
            for i in self.entryFrame1.winfo_children():
                i.delete(0 , ctk.END)
                self.entry_insertion(preset)

        print(count)
        print(kernel_presets.get(preset)[1][1])

    def entry_insertion(self, preset):
        count = 0
        for i in self.entryFrame1.winfo_children():
            i.insert(0 , kernel_presets.get(preset)[1][count])
            count += 1
    def checkBox2(self):
        if self.checkBox.get() == 1:
            self.scale1.configure(state="disabled")
            self.scaleLabel1.configure(text="0")
            # self.scale1.configure(button_color="gray")
        else:
            self.scale1.configure(state="normal")
            self.scaleLabel1.configure(text=int(self.scale1.get()))
            # self.scale1.configure(button_color=None)

    def apply_dim(self, dim):
        if self.lastDim == dim:
            return
        self.destroy_entries()
        self.entries(dim)
        
    def destroy_entries(self):
        for i in self.entryFrame1.winfo_children():
            i.destroy()

    def entries(self, dim):
        for i in range(dim):
            for j in range(dim):
                entry = ctk.CTkEntry(self.entryFrame1, width=35, fg_color="#1C1C1C")
                entry.grid(row=i, column=j, padx=7, pady=7)
        self.lastDim = dim

    def widget_rankFilter(self):
        self.editFrame = ctk.CTkFrame(self.filterFrame, fg_color="#1C1C1C")
        self.editFrame.grid(row=0, column=0, columnspan=5, padx=40, pady=5)

        self.labelFrame1 = ttk.Labelframe(self.editFrame, text="Select Preset",
                                           borderwidth=3
                                           )
        self.labelFrame1.grid(row=0, column=0, pady=7, padx=15)
        values=["Min Filter", "Median Filter", "Max Filter"]
        self.comboBox1 = ctk.CTkComboBox(
            self.labelFrame1,
            values=values,
            state="readonly",
            # command=
            )
        self.comboBox1.grid(row=0, column=0)

        self.bigFrame = ctk.CTkFrame(self.editFrame)
        self.bigFrame.grid(row=1, column=0, pady=15)

        self.scaleFrame1 = ctk.CTkFrame(self.bigFrame)
        self.scaleFrame1.grid(row=0, column=0, pady=15, padx=15)

        self.scaleLabel1 = ctk.CTkLabel(self.scaleFrame1, text="0", width=40)
        self.scaleLabel1.grid(row=0, column=0, padx=10)

        self.scaleLabel2 = ctk.CTkLabel(self.scaleFrame1, text="Scale")
        self.scaleLabel2.grid(row=0, column=2, padx=10)

        self.scale1 = ctk.CTkSlider(
            self.scaleFrame1,
            width=150,
            from_=0,
            to=51,
            number_of_steps=51,
            command=lambda v: self.scaleLabel1.configure(text=int(v))
            )
        self.scale1.grid(row=0, column=1, padx=5)
        self.scale1.set(0)

        self.scaleFrame2 = ctk.CTkFrame(self.bigFrame)
        self.scaleFrame2.grid(row=1, column=0, pady=15, padx=15)

        self.scaleLabel3 = ctk.CTkLabel(self.scaleFrame2, text="0", width=40)
        self.scaleLabel3.grid(row=0, column=0, padx=10)

        self.scaleLabel4 = ctk.CTkLabel(self.scaleFrame2, text="Rank")
        self.scaleLabel4.grid(row=0, column=2, padx=10)

        self.scale2 = ctk.CTkSlider(
            self.scaleFrame2,
            width=150,
            from_=0,
            to=2600,
            number_of_steps=2600,
            command=lambda v: self.scaleLabel3.configure(text=int(v))
            )
        self.scale2.grid(row=0, column=1, padx=5)
        self.scale2.set(0)
    
    def widget_modeFitler(self):
        self.editFrame = ctk.CTkFrame(self.filterFrame, fg_color="#1C1C1C")
        self.editFrame.grid(row=0, column=0, columnspan=5, padx=30, pady=15)

        self.scaleFrame1 = ctk.CTkFrame(self.editFrame)
        self.scaleFrame1.grid(row=0, column=0, padx=10, pady=10)

        self.scaleLabel1 = ctk.CTkLabel(self.scaleFrame1, text="50")
        self.scaleLabel1.grid(row=0, column=0, padx=10, pady=5)

        self.scaleLabel2 = ctk.CTkLabel(self.scaleFrame1, text="Radius")
        self.scaleLabel2.grid(row=0, column=2, padx=10)

        self.scale1 = ctk.CTkSlider(
            self.scaleFrame1,
            from_=0,
            to=50,
            command=lambda v: self.scaleLabel1.configure(text=int(v))
            )
        self.scale1.grid(row=0, column=1)

    def apply_filters(self, radius):
        new_img = self.img.filter(ImageFilter.BoxBlur(radius))
        img_ctk = ctk.CTkImage(light_image=new_img, dark_image=new_img, size=(400,400))
        self.photoLabel.configure(image=img_ctk)

    def apply_filter(self, preset, radius, scale=0, offset=0):
        if preset == "Box Blur":
            new_img = apply_boxBlur(self.img, radius)
            self.update_img(new_img)
        if preset == "Kernel":
            pass
            # new_img = apply_
        # widget_dict = {
        #     "Box Blur": apply_boxBlur,
        #     "Kernel": apply_kernel,
        #     "Gaussian Blur": apply_gaussianBlur,
        #     "Unsharp Mask": apply_unsharpenMask,
        #     "Rank Filter": apply_rankFilter,
        #     "Mode Filter": apply_modeFitler
        # }
            
    def update_img(self, img):
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(400,400))
        self.photoLabel.configure(image=img_ctk)

    def reset_img(self):
        self.img_copy = self.img_copy.resize((500,500))
        img_ctk = ctk.CTkImage(light_image=self.img_copy, dark_image=self.img_copy, size=(400,400))
        self.photoLabel.configure(image=img_ctk)

def display_img(self: Process, image):
    img = image
    self.photoLabel.configure(image=img)

def destroyer(garbage):
    garbage.destroy()
    return

def get_dir():
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
        title="Choose an image.."
    )
    return file_path


def check_path(file_path):
    format = os.path.splitext(file_path)[-1][1:]
    if not file_path:
        CTkMessagebox.messagebox(
            title="ERROR",
            text="Please choose a path",
            sound="on",
            )
        return
    if not os.path.exists(file_path):
        CTkMessagebox.messagebox(
            title="ERROR",
            text="Please enter the correct path",
            sound="on",
            )
        return 
    if format not in {"png"}:
        CTkMessagebox.messagebox(
            title="ERROR",
            text="Please choose a supported format",
            sound="on",
            )
        return 
    return True
if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    Main()
