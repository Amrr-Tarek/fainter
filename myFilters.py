import os
from PIL import Image, ImageFilter, ImageOps, ImageTk

# cwd = os.path.dirname(os.path.abspath(__file__))
# os.chdir(cwd)

# Also see: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
supported = {"png", "bmp", "jpeg", "jpg", "ico"}  # Wanted: WebP, GIF, TIFF
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
    "SMOOTH_MORE",  # END OF PREDEFINED (USE KERNEL AND ADD THEM AS PRESETS)
    "BoxBlur",  # radius x, y or 1 for both > 0
    "GaussianBlur",  # radius x, y or 1 for both > 0
    "UnsharpMask",  # radius > 0, percent > 0, threshold -> 0:255
    "Kernel",  # L AND RGB ONLY !!!
    "RankFilter",  # size: odd number >= 3, rank -> 0: (size * size / 2)
    "MedianFilter",  # with rank
    "MinFilter",  # with rank
    "MaxFilter",  # with rank
    "ModeFilter",  # size > 0 to 50 for performance
]
presets = [
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
]
# هين
filters = [
    "Box Blur",
    "Gaussian Blur",
    "Unsharp Mask",
    "Kernel",
    "Rank Filter",
    # "Median Filter",
    # "Min Filter",
    # "Max Filter",
    "Mode Filter",
]


def process_image(img: Image.Image, amt):
    myDict = {
        "Box Blur": 0,
        "gaussian blur": 0,
        "Unsharp Mask": 0,
        "Kernel": 0,
        "Rank Filter": 0,
        "Mode Filter": 0,
    }
    # filter = myDict.get("gaussian blur")

    return img.filter(ImageFilter.GaussianBlur(amt))


"""
Main:       Put the same dictionary and on each filter.. there is a function to call
            each function adds the desired widgets
            Apply button will call the process_image here.. and checks for what filter is used and based on it it takes the valeus from the sliders and numbers, etc

myFilters:  Put the same dictionary and on each filter.. apply the attr wanted (this should be the easiest)
"""

# https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
# Usage: ImageOps.FILTER(img)
ops = [
    "autocontrast()",
    "colorize()",
    "crop()",
    "scale()",
    "SupportsGetMesh",
    "deform()",
    "equalize()",
    "expand()",
    "flip()",
    "grayscale()",
    "invert()",
    "mirror()",
    "posterize()",
    "solarize()",
    "exif_transpose()",
    "Resize relative to a given size:",
    "contain()",
    "cover()",
    "fit()",
    "pad()",
]

# https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
# Usage: img.filter(ImageFilter.FILTER())


"""
Program cons: No support for transparent
Can be done by splitting the rgba channels, mergin rgb, applying the filters, merge the rgb with the alpha channel
"""


def get_func_defaults(func):
    """_summary_

    Args:
        func (function): takes a function name

    Returns:
        dict: a dictionary of key: argument name, value: argument default (None if none)
    """
    import inspect

    signature = inspect.signature(func)
    myDict = {}

    for name, param in signature.parameters.items():
        if param.default is not inspect.Parameter.empty:
            myDict[name] = param.default
        else:
            myDict[name] = None

    return myDict


if __name__ == "__main__":
    pass
    # print(get_func_defaults(ImageFilter.Kernel))
    # original_image = Image.open("medium.png").convert(
    #     "RGB"
    # )  # Temporarily Always convert into RGB
    # apply_filter()

    # processed_image.save("output.png")

    # print(type(original_image))
    # print(type(processed_image))
    # print(type("sh"))
    # process_image("medium.png")
