from array import array
import numpy as np
from PIL import Image

CHAR_ARRAY_GRAYSCALE = ' abcdefghijklmnopqrstuvwxyz' # 27
CHAR_ARRAY_COLOR = ' abcdefghijklmnopqrstuvwxyz!@#$%^&*()-=<>?[]/' # 45

COLOR_CHANNEL_DICT = {
    'red': {
        'length': 9,
        'phrase': '   <o)   ',
        'unprocessed_phrase': 'iipp=lx>^'
    },
    'green': {
        'length': 9,
        'phrase': '   /) )  ',
        'unprocessed_phrase': 'w>lzixv*<'
    },
    'blue': {
        'length': 9,
        'phrase': ' ==#===  ',
        'unprocessed_phrase': 'fa>r-$@go'
    }
}

WORD_LENGTH_GRAYSCALE = 4
LOWER_BOUND_PIXEL_VALUE = 0
UPPER_BOUND_PIXEL_VALUE = 255

def GenerateRandomGrayscaleImage(num_rows: int, num_cols: int) -> np.ndarray:
    # Set the RNG seed for consistent results, so debugging is easier
    # Change the seed or comment out this line as desired
    np.random.seed(0)
    flat_array = np.random.randint(0, 256, num_rows * num_cols)
    return flat_array.reshape(num_rows, num_cols)

# LoadImage -- necessary to test with existing image for color example with 3 channels
def LoadImage(input_filepath: str) -> np.ndarray:
    img = Image.open(input_filepath)
    img.load() # Allocates storage for the image and loads the pixel data.
    image_np_array = np.asarray(img)
    return image_np_array

def SaveImage(image_np_array: np.ndarray, output_filepath: str):
    img = Image.fromarray(image_np_array)
    img.save(output_filepath)


def initialize_grouping_dict(length):
    grouping_dict = {}
    for i in range(length):
        grouping_dict[i] = 0
    return grouping_dict


def apply_index_offset(flattened_matrix, modification_dict, channel=None):
    
    if channel:
        channel_phrase_length = COLOR_CHANNEL_DICT[channel]['length']
    else:
        channel_phrase_length = WORD_LENGTH_GRAYSCALE

    modified_matrix = flattened_matrix
    
    for z in range(channel_phrase_length):
        # Identify the value to offset by
        offset_value = modification_dict[z]
        
        # Iterate over the index and value at that index in modified matrix, in order to distribute the offset value
        for i, x in enumerate(modified_matrix):
            if i % channel_phrase_length == z: 
            # Loops over every Nth index where N is the length of the phrase: 0, 4, 8, 12//1, 5, 9, 13//2, 6, 10, 14//3, 7, 11, 15

                # Identify how much the current value can be incremented or decremented:
                max_increment = UPPER_BOUND_PIXEL_VALUE - x 
                max_decrement = x

                while offset_value != 0: # while it's not 0, continue adding or subtracting
                    if x > LOWER_BOUND_PIXEL_VALUE and x < UPPER_BOUND_PIXEL_VALUE:

                        # Safe to add full value to current index:
                        # offset value is positive, and less than the difference between current value and 255
                        if offset_value > 0 and offset_value <= max_increment:
                            modified_matrix[i] += offset_value
                            offset_value = 0 # Full value has been added, so move along

                        # Greater than the max_increment value, keep looping and add remainder to the next index
                        if offset_value > 0 and offset_value > max_increment:
                            modified_matrix[i] += max_increment
                            difference = offset_value - max_increment
                            offset_value = difference

                        # Safe to subtract full value from current index
                        if offset_value < 0 and max_decrement + offset_value > 0:
                            modified_matrix[i] += offset_value
                            offset_value = 0

                        # Only part of the offset_value can be subtracted, must continue subtracting for next
                        if offset_value < 0 and offset_value is 1:
                            difference = offset_value + max_decrement
                            offset_value += max_decrement
                            modified_matrix[i] -= difference

                        # Consider the case the offset_value exactly equals max
                        if offset_value < 0 and offset_value + max_decrement == 0:
                            modified_matrix += offset_value
                            offset_value = 0

    return modified_matrix


def encode_grayscale_image(message_length):
    matrix = GenerateRandomGrayscaleImage(message_length, message_length)
    group_sum_dict = initialize_grouping_dict(message_length) # Initializes dict with message_length keys and all values starting at 0

    phrase = 'crow'
    flat_array = matrix.flatten()
    array_length = len(flat_array)

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

    unprocessed_word = ''.join(char_list)
    modification_dict = {}

    # Set values for modification_dict keys based on difference between target and actual word
    for i in range(len(unprocessed_word)):
        difference = CHAR_ARRAY_GRAYSCALE.find(unprocessed_word[i]) - CHAR_ARRAY_GRAYSCALE.find(phrase[i])
        modification_dict[i] = -(difference)

    modified_flattened_array = apply_index_offset(flat_array, modification_dict)
    final_image_array = modified_flattened_array.astype('uint8')
    SaveImage(final_image_array, 'grayscale_test.png')

    return final_image_array


def encode_color_image(color_channel_len_dict):
    color_image_matrix = []
    image_matrix_color = LoadImage('kingfisher.jpeg').astype('int32')

    channel_dict = {
        'red': image_matrix_color[:, :, 0],
        'green': image_matrix_color[:, :, 1],
        'blue': image_matrix_color[:, :, 2]
    }

    for channel in color_channel_len_dict:
        message_length = color_channel_len_dict[channel]['length'] # Phrase length
        phrase = color_channel_len_dict[channel]['phrase'] # Target phrase
        group_sum_dict = initialize_grouping_dict(message_length) # Initializes dict with keys for each char of phrase, value of message length
        flattened_array = channel_dict[channel].flatten()
        array_length = len(flattened_array)

        # Create sums for each character from matrix into group_sum_dict
        for i in range(array_length):
            # Sum values for each character dict, every nth index where n is the index of the character in the phrase
            group_sum_dict[i % message_length] += flattened_array[i]

        unprocessed_word = color_channel_len_dict[channel]['unprocessed_phrase']
        modification_dict = {}

        # Set values for modification_dict keys based on difference between target and actual word
        for i in range(len(unprocessed_word)):
            difference = CHAR_ARRAY_COLOR.find(unprocessed_word[i]) - CHAR_ARRAY_COLOR.find(phrase[i])
            modification_dict[i] = -(difference)

        modified_flattened_array = apply_index_offset(flattened_array, modification_dict, channel)
        processed_image_array = modified_flattened_array.astype('uint8')
        SaveImage(processed_image_array, f'grayscale_test_{channel}.png')
        color_image_matrix.append(processed_image_array)

    rgb = np.dstack((color_image_matrix[0], color_image_matrix[1], color_image_matrix[2])).astype(np.uint8)
    rgb_shaped = rgb.reshape(image_matrix_color.shape)
    SaveImage(rgb_shaped, 'color_image_name.png')

    return


def main():
    print('Encoding grayscale image: ', encode_grayscale_image(WORD_LENGTH_GRAYSCALE))
    print('Encoding color image: ', encode_color_image(COLOR_CHANNEL_DICT))
    return

if __name__ == "__main__":
    main()
