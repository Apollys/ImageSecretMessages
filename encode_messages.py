from array import array
import numpy as np
from PIL import Image

CHAR_ARRAY_GRAYSCALE = ' abcdefghijklmnopqrstuvwxyz' # 27
CHAR_ARRAY_COLOR = ' abcdefghijklmnopqrstuvwxyz!@#$%^&*()-=<>?[]' # 44
# "   <o)   "  000 - 39 - 15 - 36 - 000
# "   /) )  "  000 - 44 - 36 - 0 - 36 - 00
# " ==#===  " 0-38-38-29-38-38-38-00

# ['iipp=lx>^', 'w>lzixv*<', 'fa>r-$@go']

# f!h]<ap%?

# Got: ['uubbmrene', 'aafwrkehc', 'ysetbvyli']
COLOR_CHANNEL_DICT = {
    'RED': {
        'length': 9,
        'phrase': 'hipp=lx>^', # '   <o)   '
        'unprocessed_phrase': 'iipp=lx>^' # hroiirixc
    }
    # 'GREEN': {
    #     'length': 9,
    #     'phrase': '',
    #     'unprocessed_phrase': 'w>lzixv*<'
    # },
    # 'BLUE': {
    #     'length': 9,
    #     'phrase': '',
    #     'unprocessed_phrase': 'fa>r-$@go'
    # }
}

WORD_LENGTH_GRAYSCALE = 4
LOWER_BOUND_PIXEL_VALUE = 0
UPPER_BOUND_PIXEL_VALUE = 255

WORD_LENGTH_COLOR = 9 # test, remove later

def GenerateRandomGrayscaleImage(num_rows: int, num_cols: int) -> np.ndarray:
    # Set the RNG seed for consistent results, so debugging is easier
    # Change the seed or comment out this line as desired
    np.random.seed(0)
    flat_array = np.random.randint(0, 256, num_rows * num_cols)
    # print('flat_array: ', flat_array.reshape(4, 4))
    return flat_array.reshape(num_rows, num_cols)

def GenerateTestImage() -> np.ndarray:
    return np.ones((5, 5, 3), dtype='int16')

print('generate test image: ', GenerateTestImage()) # All 1s

# LoadImage -- necessary to test with existing image for color example with 3 channels
def LoadImage(input_filepath: str) -> np.ndarray:
    img = Image.open(input_filepath)
    img.load() # Allocates storage for the image and loads the pixel data.
    image_np_array = np.asarray(img)
    return image_np_array

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
    # Takes in flattened matrix and returns a modified flattened matrix with updated index values 
    # to get actual word

    # Iterate through each letter and apply values from modification_dict if within constraints (0-255)

    # modification_dict = {
    #     0: 11, 
    #     1: -16, 
    #     2: 10, 
    #     3: 1
    # }

    # flattened_matrix:  [172  47 117 192  67 251 195 103   9 211  21 242  36  87  70 216] # Start out with this
    # Want to achieve this: [183  31 127 193  67 251 195 103   9 211  21 242  36  87  70 216]

    modified_matrix = flattened_matrix
    
    for z in range(WORD_LENGTH_GRAYSCALE): # 4
        print('z: ', z)
        add_value = modification_dict[z] # Each run through -- 11, then -16, then 10, then 1
        # print('\nValue to be modified: ' + str(add_value)) # ******
        for i, x in enumerate(modified_matrix):
            if i % WORD_LENGTH_GRAYSCALE == z: # Loops over indices 0, 4, 8, 12//1, 5, 9, 13//2, 6, 10, 14//3, 7, 11, 15
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
                        if add_value > 0 and add_value > max_increment:
                            difference = add_value - max_increment
                            modified_matrix[i] += difference

                        # Safe to subtract full value from current index
                        if add_value < 0 and max_decrement + add_value > 0:
                            modified_matrix[i] += add_value
                            add_value = 0

                        # Only part of the add_value can be subtracted, must continue subtracting for next
                        if add_value < 0 and add_value is 1:
                            difference = add_value + max_decrement # Figure out add value that can be added to this index -- -5 + 2 = -3
                            add_value += max_decrement # -2 + 3 = -3 --> moving closer to 0, update add_value so it can be reused until it hits 0
                            modified_matrix[i] -= difference

    return modified_matrix

# Try to offset by just 1 index 
# Change first letter to be 1 letter further
# Make that target message, pass into encoder function and see what happens
# ab is what I have. Target is going to be bb.
# hi -> ii
# Pass into red channel, into encoder function that run it and see after encode message ii into there, what message output

def process_grayscale_image(message_length):
    # Takes in a message length, generates a random GenerateRandomGrayscaleImage 
    # Start matrix = [172  47 117 192  67 251 195 103   9 211  21 242  36  87  70 216]
    # Ending matrix = [[183, 31, 127, 193], [67, 251, 195, 103], [9, 211, 21, 242], [36, 87, 70, 216]]

    matrix = GenerateRandomGrayscaleImage(message_length, message_length) # Start matrix
    group_sum_dict = initialize_grouping_dict(message_length) # Initializes dict with message_length keys and all values starting at 0

    phrase = 'crow'
    flat_array = matrix.flatten()
    array_length = len(flat_array)

    # sum for each group in message_length (3)
    for i in range(array_length):
        group_sum_dict[i % message_length] += flat_array[i]

    char_list = ['' for length in range(message_length)]
    test_dict = {}
    len_grayscale_alphabet = len(CHAR_ARRAY_GRAYSCALE)

    # Decode:
    for key in group_sum_dict:
        character_value = group_sum_dict[key] % len_grayscale_alphabet # Number of chars in cryptograph
        test_dict[key] = character_value
        character = CHAR_ARRAY_GRAYSCALE[character_value]
        char_list[key] = character

    word = ''.join(char_list) # Unprocessed word

    modification_dict = {}
    # modification_dict = {
    #     0: -11, 
    #     1: 16, 
    #     2: -10, 
    #     3: -1
    # }

    # Set values for modification_dict keys based on difference between target and actual word
    for i in range(len(word)):
        difference = CHAR_ARRAY_GRAYSCALE.find(word[i]) - CHAR_ARRAY_GRAYSCALE.find(phrase[i])
        modification_dict[i] = -(difference)

    modified_flattened_array = apply_index_offset_greyscale(flat_array, modification_dict)
    final_image_array = modified_flattened_array.astype('uint8')
    SaveImage(final_image_array, 'grayscale_test.png')
    return final_image_array

print('Printing modified flattened array: ', process_grayscale_image(WORD_LENGTH_GRAYSCALE))


def apply_index_offset_color(flattened_matrix, modification_dict, channel):
    # Takes in flattened matrix and returns a modified flattened matrix with updated index values 
    # to get actual word

    # flattened_matrix:  [*172  47 117 192  *67 251 195 103   *9 211  21 242  *36  87  70 216] # Ex. start out with this
    # Want to achieve this: [183  31 127 193  67 251 195 103   9 211  21 242  36  87  70 216]

    # unprocessed word:  ysetbvyli
    # modification_dict:  {0: -25, 1: 19, 2: 33, 3: 9, 4: 36, 5: 16, 6: 13, 7: -12, 8: -9}
    # After applying change, I am applying changes to parts of image that don't need to be changed
    print('***flattened_matrix: ', flattened_matrix)
    channel_phrase_length = COLOR_CHANNEL_DICT[channel]['length']
    modified_matrix = flattened_matrix
    

    # For each letter - c, r, o, w
    for z in range(channel_phrase_length): # Function "freezes"  when z = 5, i = 5 and x = 251
        # print('iterating through values in range function...') # Does this 6 times then hangs on the 7th

        # Identify the value we need to offset by
        offset_value = modification_dict[z] # Each run through -- 11, then -16, then 10, then 1
        # print('offset value: ', offset_value)
        # print('\nValue to be modified: ' + str(offset_value)) # ******

        # Iterate over the index and value at that index in modified matrix, in order to distribute the offset value
        for i, x in enumerate(modified_matrix):
            # print('i: ', str(i))
            # print('x: ', str(x))
            # i is index 8, value is 9

            # Last i and x values: i: 5, x: 251 when z is 5
            # 5 % 9 == 5? Yes in this case
            if i % channel_phrase_length == z: 
            # Loops over every Nth index where N is the length of the phrase: 0, 4, 8, 12//1, 5, 9, 13//2, 6, 10, 14//3, 7, 11, 15

                # print("if condition satisfied, looping over every 9th letter")
                # print("do something with x " + str(x)) # ******

                # Identify how much the current value can be incremented or decremented:
                max_increment = UPPER_BOUND_PIXEL_VALUE - x 
                
                # The max number of times this number can be incremented:
                # 255 - x where x is the current value. In this case it's 251, so 255 - x means max_increment is 4.
                max_decrement = x # This is 251, in this example

                # Errors when offset is 18 -- on the 5th index when the letter being processed is 'r'!
                while offset_value != 0: # while it's not 0, continue adding or subtracting
                    if x > LOWER_BOUND_PIXEL_VALUE and x < UPPER_BOUND_PIXEL_VALUE:
                        # Within range of 0-255, can be incremented and decremented
                        # print('within range of 0-255...')

                        # Safe to add full value to current index:
                        # offset value is positive, and less than the difference between current value and 255
                        # ex. offset value is 3, and max_increment is 4 -- safely add
                        if offset_value > 0 and offset_value <= max_increment:
                            ## not going into here when error happens
                            modified_matrix[i] += offset_value
                            offset_value = 0 # Full value has been added, so move along

                        # Greater than the max_increment value, keep looping and add remainder to the next index
                        # offset_value exceeds max increment value -- need to try and distribute remainder to next index
                        if offset_value > 0 and offset_value > max_increment:
                            # modified_matrix[i] += difference # Errors here ? 
                            modified_matrix[i] += max_increment # add 4
                            # Declare difference
                            difference = offset_value - max_increment # 14 - 4 = 10 
                            offset_value = difference # remainder -- update offset value to this
                            
                            #  14 - 4 = 10, keep trying this value with next index
                            # The error occurs when we're trying to encode the channel value and have a remainder to carry over...
                            
                        # Safe to subtract full value from current index
                        if offset_value < 0 and max_decrement + offset_value > 0:
                            # Doesn't go into here either
                            modified_matrix[i] += offset_value
                            offset_value = 0

                        # Only part of the offset_value can be subtracted, must continue subtracting for next
                        if offset_value < 0 and offset_value is 1:
                            difference = offset_value + max_decrement # Figure out add value that can be added to this index -- -5 + 2 = -3
                            offset_value += max_decrement # -2 + 3 = -3 --> moving closer to 0, update offset_value so it can be reused until it hits 0
                            modified_matrix[i] -= difference

                        # Consider the case the offset_value exactly equals max
                        if offset_value < 0 and offset_value + max_decrement == 0: # If offset_value is -3, max_decrement is 3, exactly evens out
                            modified_matrix += offset_value
                            offset_value = 0

    print('***modified_matrix: ', modified_matrix)

    return modified_matrix


def process_color_image(color_channel_len_dict):
    color_image_matrix = []
    color_alphabet_length = len(CHAR_ARRAY_COLOR)

    for channel in color_channel_len_dict:
        message_length = color_channel_len_dict[channel]['length']
        phrase = color_channel_len_dict[channel]['phrase']

        # matrix = GenerateRandomGrayscaleImage(message_length, message_length) # Generated test matrix for a single channel to test offset
        matrix = GenerateTestImage() # LoadImage('kingfisher.jpeg').astype('int32')
        group_sum_dict = initialize_grouping_dict(message_length) # Initializes dict with value of channel length
        flat_array = matrix.flatten()
        array_length = len(flat_array) # Total number of values across all channels -- in the case of 9 x 9, it's 81

        # Create sums for each character from matrix
        for i in range(array_length):
            group_sum_dict[i % message_length] += flat_array[i] # Sum values for each character dict, every nth index where n is the index of the character in the phrase

        char_list = ['' for length in range(message_length)]
        test_dict = {}

        # Decode:
        for key in group_sum_dict:
            # print("key: ", key) # for the position of each character, 0-8
            character_value = group_sum_dict[key] % color_alphabet_length # Number of chars in cryptograph
            # print("character value: ", character_value)
            test_dict[key] = character_value
            character = CHAR_ARRAY_COLOR[character_value]
            char_list[key] = character

        # unprocessed_word = ''.join(char_list)
        unprocessed_word = color_channel_len_dict[channel]['unprocessed_phrase']
        print('unprocessed word: ', unprocessed_word)
        modification_dict = {}

        # CHAR_ARRAY_COLOR = ' abcdefghijklmnopqrstuvwxyz!@#$%^&*()-=<>?[]'

        # Set values for modification_dict keys based on difference between target and actual word
        for i in range(len(unprocessed_word)):
            difference = CHAR_ARRAY_COLOR.find(unprocessed_word[i]) - CHAR_ARRAY_COLOR.find(phrase[i])
            modification_dict[i] = -(difference)

        print('modification_dict: ', modification_dict)

        # Behaviour here is probably not as intended
        modified_flattened_array = apply_index_offset_color(flat_array, modification_dict, channel) # matrix for single channel
        print('modified flattened array get **')
        processed_image_array = modified_flattened_array.astype('uint8')
        SaveImage(processed_image_array, f'grayscale_test_{channel}.png')
        # color_image_matrix.append(processed_image_array)

    # rgb = np.dstack((r,g,b))
    # rgb = np.dstack((color_image_matrix[0], color_image_matrix[1], color_image_matrix[2]) * 255.999).astype(np.uint8)
    # SaveImage(rgb, 'color_test_12345.png') # For debugging purposes if trying to decode
    # ValueError: zero-dimensional arrays cannot be concatenated

    return # color_image_matrix


def main():
    # process_grayscale_image(WORD_LENGTH_GRAYSCALE)
    # process_color_image(COLOR_CHANNEL_DICT)
    print('Printing modified flattened color array: ', process_color_image(COLOR_CHANNEL_DICT))
    return

if __name__ == "__main__":

#     # matrix = LoadImage('kingfisher.jpeg').astype('int32')
#     # print('matrix: ', matrix)
    main()
