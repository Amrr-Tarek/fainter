import os

# import tkinter as tk

# root = tk.Tk()  # window

# root.geometry("854x480")
# root.title("This is a test")

# root.mainloop()


from PIL import Image, ImageFilter

cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

# Also see: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
supported = {"png", "bmp", "jpeg", "jpg", "ico"}  # Wanted: WebP, GIF, TIFF


file_path = ""
format = file_path.split(".")[-1]
print(f"File Path: {file_path}")


if not file_path:
    print("Empty file path\nExiting the program..")
    exit()
if format not in supported:
    print(f'Unsupported File Format: ".{format}"')
    exit()
else:
    print(f'Good Format ".{format}"')


# before = Image.open("fainter/medium.png").convert("RGB")
# after = before.filter(ImageFilter.FIND_EDGES)

# after.save("fainter/output.png")

# https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
filters = [
    "BLUR",
    "CONTOUR",
    "DETAIL",
    "EDGE_ENHANCE",
    "EDGE_ENHANCE_MORE",
    "EMBOSS",
    "FIND_EDGES",
    "SHARPEN",
    "SMOOTH",
    "SMOOTH_MORE",
    "GaussianBlur",
    "BoxBlur",
    "RankFilter",
    "MedianFilter",
    "MinFilter",
    "MaxFilter",
    "ModeFilter",
    "UnsharpMask",
    "Kernel",
]
