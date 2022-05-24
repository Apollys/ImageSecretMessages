import numpy as np
from PIL import Image

CHAR_ARRAY = ' abcdefghijklmnopqrstuvwxyz'
WORD_LENGTH = 4

LOWER_BOUND_PIXEL_VALUE = 0
UPPER_BOUND_PIXEL_VALUE = 255

def GenerateRandomGrayscaleImage(num_rows: int, num_cols: int) -> np.ndarray:
    # Set the RNG seed for consistent results, so debugging is easier
    # Change the seed or comment out this line as desired
    np.random.seed(0)
    flat_array = np.random.randint(0, 256, num_rows * num_cols)
    # print('flat_array: ', flat_array.reshape(4, 4))
    return flat_array.reshape(num_rows, num_cols)

def SaveImage(image_np_array: np.ndarray, output_filepath: str):
    img = Image.fromarray(image_np_array)
    img.save(output_filepath)

# Input image array
# GenerateRandomGrayscaleImage(4, 4)
# [172  47 117 192  67 251 195 103   9 211  21 242  36  87  70 216]
# [[172  47 117 192]
#  [ 67 251 195 103]
#  [  9 211  21 242]
#  [ 36  87  70 216]]

def initialize_grouping_dict(length):
    grouping_dict = {}
    for i in range(length):
        grouping_dict[i] = 0
    return grouping_dict

# Offset by:
# -10, +16, -10, -1
# Desired index:
# 4, 19, 16, 24
# {0: 4, 1: 19, 2: 16, 3: 24}

# Actual index: 
# 14, 3, 26, 25
# {0: 14, 1: 3, 2: 26, 3: 25}

def apply_index_offset_greyscale(flattened_matrix, modification_dict):
    print('entered apply offset greyscale function')
    # Takes in flattened matrix and returns a modified flattened matrix with updated index values 
    # to get actual word

    # Go through each letter (every Nth index, where N is the length of the word or phrase) and apply
    # values from modification_dict as long as within constraints -- 0 to 255

    # modification_dict = {
    #     0: 11, 
    #     1: -16, 
    #     2: 10, 
    #     3: 1
    # }

    # flattened_matrix:  [172  47 117 192  67 251 195 103   9 211  21 242  36  87  70 216] # Start out with this
    # Want to achieve this: [183  31 127 193  67 251 195 103   9 211  21 242  36  87  70 216]

    modified_matrix = flattened_matrix
    # Loop values of flattened matrix
    # Check that the current index value is within lower/upper bounds
    # If negative, check if I can subtract. If positive, check if I can add. Keep doing this through all items in the matrix until the value
    # in the modification dict is empty
    for z in range(WORD_LENGTH): # 4
        add_value = modification_dict[z] # Each run through -- 11, then -16, then 10, then 1
        # print('\nValue to be modified: ' + str(add_value)) # ******
        for i, x in enumerate(modified_matrix):
            if i % WORD_LENGTH == z: # Loops over indices 0, 4, 8, 12//1, 5, 9, 13//2, 6, 10, 14//3, 7, 11, 15
                # print("do something with x " + str(x)) # ******
                max_increment = UPPER_BOUND_PIXEL_VALUE - x
                max_decrement = x
                while add_value != 0: # while it's not 0, continue adding or subtracting
                    if x > LOWER_BOUND_PIXEL_VALUE and x < UPPER_BOUND_PIXEL_VALUE:
                        # Within range, can be incremented and decremented

                        # Safe to add full value to current index
                        if add_value > 0 and add_value <= max_increment:
                            modified_matrix[i] += add_value
                            add_value = 0 # Full value has been added, so move along
                        
                        # Greater than the max)increment value, keep looping and add remainder to the next index
                        elif add_value > 0 and add_value > max_increment:
                            difference = add_value - max_increment
                            modified_matrix[i] += difference

                        # Safe to subtract full value from current index
                        elif add_value < 0 and max_decrement + add_value > 0:
                            modified_matrix[i] += add_value
                            add_value = 0

                        # Only part of the add_value can be subtracted, must continue subtracting for next
                        elif add_value < 0 and add_value is 1:
                            difference = add_value + max_decrement # Figure out add value that can be added to this index -- -5 + 2 = -3
                            add_value += max_decrement # -2 + 3 = -3 --> moving closer to 0, update add_value so it can be reused until it hits 0
                            modified_matrix[i] -= difference
                        else:
                            print("bigger poo")

    final_image_array = modified_matrix.astype('uint8')
    # final_image_array = flattened_matrix.astype('uint8')
    print('flattened_matrix: ', flattened_matrix)
    SaveImage(final_image_array, 'test_output_encoder4.png')
    return modified_matrix

def process_grayscale_image(message_length):
    # Takes in a greyscale 
    # Start matrix = [172  47 117 192  67 251 195 103   9 211  21 242  36  87  70 216]
    # Ending matrix = [[183, 31, 127, 193], [67, 251, 195, 103], [9, 211, 21, 242], [36, 87, 70, 216]]

    matrix = GenerateRandomGrayscaleImage(message_length, message_length)
    group_sum_dict = initialize_grouping_dict(message_length)

    phrase = 'crow'
    flat_array = matrix.flatten()
    print('flat_array: ', flat_array)
    array_length = len(flat_array)

    # sum for each group in message_length (3)
    for i in range(array_length):
        group_sum_dict[i % message_length] += flat_array[i]
    print('\nWith knowledge of the length of the message, sum the value of each interval of index')
    print('group_sum_dict -- : ', group_sum_dict)
    # {0: 762, 1: 771, 2: 5641}

    char_list = ['' for length in range(message_length)]
    test_dict = {}
    # Assuming ordered, decode:
    for key in group_sum_dict:
        character_value = group_sum_dict[key] % 27 # Number of chars in cryptograph
        test_dict[key] = character_value
        character = CHAR_ARRAY[character_value]
        char_list[key] = character

    print('test_dict: ', test_dict)
    # test_dict:  {0: 14, 1: 2, 2: 25, 3: 24}
    # CHAR_ARRAY.find('c') --> gives the index of 3

    word = ''.join(char_list)

    modification_dict = {}
    # modification_dict = {
    #     0: -11, 
    #     1: 16, 
    #     2: -10, 
    #     3: -1
    # }

    # Compare word and phrase variables using CHAR_ARRAY.find('<letter>') ??
    for i in range(len(word)):
        difference = CHAR_ARRAY.find(word[i]) - CHAR_ARRAY.find(phrase[i])
        modification_dict[i] = -(difference)

    # print(modification_dict) # {0: 11, 1: -16, 2: 10, 3: 1}

    modified_array = apply_index_offset_greyscale(flat_array, modification_dict)
    return word

print('processing grayscale image, starting word: ', process_grayscale_image(4))


# nbyx -> ymhy

# n to y: + 11
# b to m: + 11
# y to h: -17 or + 10
# x to y: + 1

# modification_dict = {
#     0: -11, 
#     1: 16, 
#     2: -10, 
#     3: -1
# }

# What we actually want: 
# n to c: -11
# b to r: +16
# y to o: -10
# x to w: -1
