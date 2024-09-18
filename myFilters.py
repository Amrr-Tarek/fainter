import os
from PIL import Image, ImageFilter, ImageOps

cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

# Also see: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
supported = {"png", "bmp", "jpeg", "jpg", "ico"}  # Wanted: WebP, GIF, TIFF




def main():
    # input
    file_path = r"D:\Courses\projects\fainter\medium.png"
    format = file_path.split(".")[-1]
    print(f"File Path: {file_path}")

    # output
    outputName = "output"
    outputFormat = "png"
    save_path = rf"D:\Courses\projects\fainter\{outputName}.{outputFormat}"
    print(save_path)

    if not file_path:
        print("Empty file path\nExiting the program..")
        exit()
    if format not in supported:
        print(f'Unsupported File Format: ".{format}"')
        exit()
    else:
        print(f'Good Format ".{format}"')

    before = Image.open(file_path).convert("RGB")  # Temporarily Always convert into RGB
    # after = before.filter(ImageFilter.FIND_EDGES)

    # after.save("output.png")
    after = ImageOps.mirror(before)
    after.save(save_path)

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

    """
    Program cons: No support for transparent
    Can be done by splitting the rgba channels, mergin rgb, applying the filters, merge the rgb with the alpha channel
    """


if __name__ == "__main__":
    main()
