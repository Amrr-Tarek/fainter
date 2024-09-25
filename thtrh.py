# def size_thres(size, minimum, maximum):
#     if all(minimum[i] <= size[i] <= maximum[i] for i in range(2)):
#         return size

#     width, height = size

#     # Maximum
#     if any(size[i] > maximum[i] for i in range(2)):
#         max_width, max_height = maximum
#         scale_factor = min(max_width / width, max_height / height)

#         new_size = tuple(round(dim * scale_factor) for dim in size)

#         if any(new_size[i] < minimum[i] for i in range(2)):
#             print("Image too wide or too thin")
#             return maximum
#         return new_size

#     # Minimum
#     elif any(size[i] < maximum[i] for i in range(2)):
#         min_width, min_height = minimum
#         scale_factor = max(min_width / width, min_height / height)

#         new_size = tuple(round(dim * scale_factor) for dim in size)

#         if any(new_size[i] > maximum[i] for i in range(2)):
#             print("Image too wide or too thin")
#             return minimum
#         return new_size


# for i in range(0, 3001, 10):
#     j = i * 9 / 16
#     if j % 10 == 0:
#         print(i, int(j))
