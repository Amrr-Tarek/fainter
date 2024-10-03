from PIL import Image, ImageFilter



def apply_boxBlur(img, radius):
    new_img = img.filter(ImageFilter.BoxBlur(radius))
    return new_img

def apply_kernel(img, size, sequence, scale=0, offset=0):
    new_img = img.filter(ImageFilter.Kernel(size, sequence, scale, offset))
    return new_img

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