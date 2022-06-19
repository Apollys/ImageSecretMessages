from email import message
import numpy as np
from PIL import Image


### GRAYSCALE ###

CHAR_ARRAY = ' abcdefghijklmnopqrstuvwxyz'
GRAYSCALE_MSG_LENGTH = 4
INPUT_FILEPATH_GRAYSCALE = 'grayscale_hidden_message.png'

# Test for encoder
COLOR_CHAR_ARRAY = ' abcdefghijklmnopqrstuvwxyz!@#$%^&*()-=<>?[]'
# GRAYSCALE_MSG_LENGTH = 9


### COLOR ###

# COLOR_CHAR_ARRAY = ' abcdefghijklmnopqrstuvwxyz'

# MSG_LENGTH_DICT = {
#     'RED': 13,
#     'GREEN': 17,
#     'BLUE': 25
# }
# INPUT_FILEPATH_COLOR = 'snowflake_hidden_message.png'

MSG_LENGTH_DICT = {
    'RED': 9,
    'GREEN': 9,
    'BLUE': 9
}

COLOR_INPUT_FILEPATH = 'color_image_name.png'


def LoadImage(input_filepath: str) -> np.ndarray:
    img = Image.open(input_filepath)
    img.load() # Allocates storage for the image and loads the pixel data.
    image_np_array = np.asarray(img)
    return image_np_array
# End LoadImage 

def SaveImage(image_np_array: np.ndarray, output_filepath: str):
    img = Image.fromarray(image_np_array)
    img.save(output_filepath)
# End SaveImage

def initialize_grouping_dict(length):
    grouping_dict = {}
    for i in range(length):
        grouping_dict[i] = 0
    return grouping_dict

def process_grayscale_image(message_length):
    matrix = LoadImage(INPUT_FILEPATH_GRAYSCALE).astype('int32')
    group_sum_dict = initialize_grouping_dict(message_length)
    flat_array = matrix.flatten()
    array_length = len(flat_array)

    # sum for each group in message_length (3)
    for i in range(array_length):
        group_sum_dict[i % message_length] += flat_array[i]

    # {0: 762, 1: 771, 2: 564}

    char_list = ['' for length in range(message_length)]

    # Assuming ordered, decode:
    for key in group_sum_dict:
        character_value = group_sum_dict[key] % 27 # Number of chars in cryptograph
        character = CHAR_ARRAY[character_value]
        char_list[key] = character

    # print('grouping_dict: ', grouping_dict)
    # {0: 'f', 1: 'o', 2: 'x'}
    # Example target sums: 7 (f), 16 (o), 25 (x)

    # for i in range(array_length):
    #     # numpy.ndarray objects can only be one data type
    #     flat_array[i] = i % 3

    # final_image_array = flat_array.reshape(matrix.shape)
    # print('final_image_array: ', final_image_array)
    # [1 2 0 1]
    # [2 0 1 2]
    # [0 1 2 0]]

    word = ''.join(char_list)
    return word

print('Hidden GRAYSCALE message: ' + process_grayscale_image(GRAYSCALE_MSG_LENGTH))

def process_color_image():
    image_matrix_color = LoadImage(COLOR_INPUT_FILEPATH).astype('int32')
    channel_dict = {
        'red': image_matrix_color[:, :, 0],
        'green': image_matrix_color[:, :, 1],
        'blue': image_matrix_color[:, :, 2]
    }

    len_char_alphabet = len(COLOR_CHAR_ARRAY)
    phrase_list = []
    colors = ['RED', 'GREEN', 'BLUE']

    for color in colors:
        color_lower = color.lower()
        flattened_array = channel_dict[color_lower].flatten()
        array_length = len(flattened_array)
        grouping_dict = initialize_grouping_dict(MSG_LENGTH_DICT[color])
        phrase = ''

        for i in range(array_length):
            grouping_dict[i % MSG_LENGTH_DICT[color]] += flattened_array[i]

        for key in grouping_dict:
            character_value = grouping_dict[key] % len_char_alphabet
            character = COLOR_CHAR_ARRAY[character_value]
            grouping_dict[key] = character
            phrase += grouping_dict[key]

        phrase_list.append(phrase)
    
    return '\n' + '\n'.join(phrase_list)

print('Hidden color message: ' + str(process_color_image()))
