# from fractions import Fraction

# myMax = (400, 600)
# mySize = (1200, 1000)


# def size_thres(size, maximum):
#     max_size = max(size)

#     coeff = max_size / maximum[size.index(max_size)]

#     return tuple(map(lambda x: x / coeff, size))


# # print(size_thres((200, 400), myMax))


# print(max(myMax, mySize))

from PIL import Image

i = 0
for method in dir(Image.Image):
    if "__" not in method:
        print(f"{i:2d}: {method}")
        i += 1
