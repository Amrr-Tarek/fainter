import os
from PIL import Image, ImageFilter, ImageOps, ImageTk

# Also see: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
supported = {"png", "bmp", "jpeg", "jpg", "ico"}  # Wanted: WebP, GIF, TIFF
# fmt: off
kernel_presets = {
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


def process_image(img: Image.Image, filter_name: str, values: list = None):
    myDict = {
        "Box Blur": apply_box,
        "Gaussian Blur": apply_gaussian,
        "Unsharp Mask": apply_unsharp,
        "Kernel": apply_kernel,
        "Rank Filter": apply_rank,
        "Mode Filter": apply_mode,
    }
    filter = myDict.get(filter_name)(values)

    return img.filter(filter)


def apply_box(radius):

    if len(radius) == 1:
        values = int(radius[0])
    else:
        values = radius

    return ImageFilter.BoxBlur(values)


def apply_gaussian(radius):
    if len(radius) == 1:
        values = int(radius[0])
    else:
        values = radius

    return ImageFilter.GaussianBlur(values)


def apply_unsharp(values):
    return ImageFilter.UnsharpMask(*values)


def apply_kernel(values):
    return ImageFilter.Kernel(*values)


def apply_rank(values):
    return ImageFilter.RankFilter(*values)


def apply_mode(values):
    return ImageFilter.ModeFilter(values[0])


# https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
# Usage: img.filter(ImageFilter.FILTER())

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


"""
Program cons:   No support for transparent
Can be done by splitting the rgba channels, mergin rgb, applying the filters, merge the rgb with the alpha channel
                Always converts to rgb before editing
"""


def get_func_defaults(func):
    """_summary_

    :args:
        func: takes a function name

    :returns:
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
