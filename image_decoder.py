import numpy as np
from PIL import Image

GREYSCALE_MSG_LENGTH = 3

MSG_LENGTH = {
    "RED": 13,
    "GREEN": 17,
    "BLUE": 25
}

CHAR_ARRAY = ' abcdefghijklmnopqrstuvwxyz'

input_filepath_greyscale = "grayscale_hidden_message.png"
input_filepath_color = "snowflake_hidden_message.png"

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

image_matrix_greyscale = LoadImage(input_filepath_greyscale).astype('int32')
# print('image_matrix: \n', image_matrix) # image_matrix.shape --> (4, 4)
# [[144 146  65 189]
#  [178  55  82 187]
#  [191 100 133 199]
#  [154 127  54  93]]

image_matrix_color = LoadImage(input_filepath_color).astype('int32')

def create_grouping_dict(length):
    grouping_dict = {}
    for i in range(length):
        grouping_dict[i] = 0
    return grouping_dict

def process_color_image(matrix, message_length):
    word = ""
    grouping_dict = create_grouping_dict(message_length)
    flat_array = matrix.flatten()
    array_length = len(flat_array)

    # sum for each group in message_length (3)
    for i in range(array_length):
        grouping_dict[i % message_length] += flat_array[i]

    # print('grouping_dict: ', grouping_dict)
    # {0: 762, 1: 771, 2: 564}

    # Assuming ordered, decode:
    for key in grouping_dict:
        character_value = grouping_dict[key] % 27
        character = CHAR_ARRAY[character_value]
        grouping_dict[key] = character

    # print('grouping_dict: ', grouping_dict)
    # {0: 'f', 1: 'o', 2: 'x'}

    # for i in range(array_length):
    #     # numpy.ndarray objects can only be one data type
    #     flat_array[i] = i % 3

    # final_image_array = flat_array.reshape(matrix.shape)
    # print('final_image_array: ', final_image_array)
    # [1 2 0 1]
    # [2 0 1 2]
    # [0 1 2 0]]

    for key in grouping_dict:
        word += grouping_dict[key]

    return word

# print('Hidden message (greyscale): ' + process_greyscale_image(image_matrix_greyscale, GREYSCALE_MSG_LENGTH))

def process_color_image(matrix):
    channel_dict = {
        "red": matrix[:, :, 0],
        "green": matrix[:, :, 1],
        "blue": matrix[:, :, 2]
    }

    phrase_list = []
    colors = ['RED', 'GREEN', 'BLUE']

    for color in colors:
        color_lower = color.lower()
        flattened_array = channel_dict[color_lower].flatten()
        array_length = len(flattened_array)
        grouping_dict = create_grouping_dict(MSG_LENGTH[color])
        phrase = ''

        for i in range(array_length):
            grouping_dict[i % MSG_LENGTH[color]] += flattened_array[i]

        for key in grouping_dict:
            character_value = grouping_dict[key] % 27 # alphabetical character, or space
            character = CHAR_ARRAY[character_value]
            grouping_dict[key] = character
            phrase += grouping_dict[key]

        phrase_list.append(phrase)
    
    return phrase_list    
    # return 'Colors ~for EXTREME~'

print('Hidden color message: ' + str(process_color_image(image_matrix_color)))
