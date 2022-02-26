# Embedding Secret Messages in Images

Images may look like assemblies of colors and shapes to our brains, but to a computer they are a collection
of numbers.  And that means if we were to interpret the numbers in a certain way, we might be able to 
discover secret messages that others have left in those images for us...

---

### What is an image?

An image is a matrix of values. The simplest case is a grayscale image, which is a 2 dimensional matrix,
each element corresponding to the brightness of a specific pixel.  Most commonly, these values will
range from 0 (black) to 255 (white).  For example, a simple 2 by 2 grayscale image:

![gray_sample_image](https://user-images.githubusercontent.com/37650759/155838036-43b15ee1-cb61-45bd-b1a3-0b1e31cd1c0c.png)

A color image is similar to a grayscale image, but with a triplet of R, G, B values for each pixel.
This means our matrix is 3 dimensional in this case.  For example:

![rgb_sample_image](https://user-images.githubusercontent.com/37650759/155838087-ecbe1140-f591-45a1-9b9f-75f10aa3effc.png)

---

### Manipulating images in Python

We can easily open, manipulate, and save images in Python. Here are some useful starter functions:

```python

import numpy as np
from PIL import Image

def LoadImage(input_filepath: str) -> np.ndarray:
    img = Image.open(input_filepath)
    img.load()
    image_np_array = np.asarray(img)
    return image_np_array
# End LoadImage 

def SaveImage(image_np_array: np.ndarray, output_filepath: str):
    img = Image.fromarray(image_np_array)
    img.save(output_filepath)
# End SaveImage
```

Once we have the image in a numpy array - in this case a 3D numpy array for RGB images, where the dimensions
are height, width, and color channel, respectively - we can see and modify all the raw pixel data.

Notes about numpy arrays:
 - Although they are called arrays, they are more like matrices.  They can have any number of dimensions.
 - Values are accessed in the same way as if you had a `list of lists of lists of ... ` in python,
   but you can use commas instead of multiple sets of brackets, e.g.: `a[0, 1, 2]`
   
A quick example, if we go back to our sample image, how would you access the blue component of the bottom left pixel?

![rgb_sample_image](https://user-images.githubusercontent.com/37650759/155838087-ecbe1140-f591-45a1-9b9f-75f10aa3effc.png)

<details>
  <summary>Answer</summary>
  
  If we call the numpy array holding the image data `image_array`, then the answer is:  `image_array[1, 0, 2]`
</details>

---

### Embedding messages in images

So an image is just a bunch of numbers.  Given a bunch of numbers, can you think of a way you would convert
those numbers into a text message?  Don't worry about how you would control the content of the message or
anything like that, just think about how you could extract some form of message from an image.

Here's a really simple way.  What if we just add up all the pixel values in an image, and then interpret
this number as a character in some way.  Let's call the sum of all pixel values `total_sum`, and then
in order to convert it into one of the 26 letters of the alphabet, we perform the operation `total_sum % 26`.
Then we say `0 = a, 1 = b, 2 = c`, and so on, thus converting our numerical value into a single letter.

Take a moment to think how you might extract a full message (let's say at least 10 characters) rather than
just a single letter from an image.  And feel free to assume the image is whatever size you like.

---

What if you wanted to include the option for capital letters as well?

---

Once you've brainstormed a little on the above questions, I'll share with you my approach.

---

### My idea

Let's start by thinking of just a grayscale image for now.  Suppose we wanted to embed a message of length 3
into our image, and let's just say our image is of size 4 by 4.  We could apply the same idea we had before,
but group the pixels into 5 different groups, one for each letter.  This might look something like:

![grouping_sample_diagram](https://user-images.githubusercontent.com/37650759/155839561-3f0ddb20-41a8-44c4-83a1-00155e4be96a.png)

Note the colors are only used to illustrate groupings, they don't correlate in any way to the image pixel colors.

So we sum up all the pixel values in blue to one value, orange to another value, and purple to a third value.
Then we map each of these from integer values to characters. But let's allow for spaces to also be included in our messages,
so instead, our mapping will be `0 = ' ', 1 = 'a', 2 = 'b', 3 = 'c', ..., 26 = 'z'`.  This means we take each group sum
and mod (`%` operator) by 27 rather than 26 now, then use our int to character mapping to retrieve the final text message.

Here's a 4x4 grayscale image with a message of length 3 embedded in it, exactly as we just discussed.  See if you can
figure out what the message is!

[grayscale_hidden_message.png](https://user-images.githubusercontent.com/37650759/155843190-484ef444-a3a2-4078-8c03-09b57783be6e.png)

Some general numpy tips:
 - Print `image_array.shape` (note no parentheses `()` after shape) rather than the whole array;
   often printing the whole array is too messy
 - For this 4x4 grayscale image, `image_array.shape` should give you `(4, 4)`
 - For a 4x4 color image, `image_array.shape` would give you `(4, 4, 3)`
 - Indexing order is row, column, color channel (optional), for example: `image_array[row_i][column_i][channel_i]` for a color image
 - Use "flattened arrays" to access elements in left-right top-bottom (reading) order, as a long 1D vector:
   `flat_array = image_array.flatten()`
 - Now you can access the fifth element by `flat_array[4]` regardless of which row or column it was in
 - Once you're done modifying elements and want to turn it back into the original dimensions, use
   `final_image_array = flat_array.reshape(input_image_array.shape)`, to turn it back into the exact
   same dimensions of `input_image_array`
 - By default, images are read into 8-bit integer values (0-255), and stored in a datatype called `uint8`
   that can only hold such values.  This gives tricky behavior when computing sums: 250 + 10 --> 4
   (because the value "wraps around", 256 becomes zero)
 - Use `image_array = LoadImage('some_image.png').astype('int32')` to avoid these overflow (or underflow!) issues

Once you've got a guess for the embedded message, click below to check if you got it:

<details>
  <summary>Check my answer</summary>
  
  ![fox_winter_drawing](https://user-images.githubusercontent.com/37650759/155842208-6f45ed7c-499c-43ca-855d-8c52be797abe.png)
  
  If you have no idea why this picture is here, you may want to go back and debug your message decoding algorithm.
  
  If you do know why this picture is here, congratulations!  Take a moment to relax and enjoy this beautiful drawing :D
</details>

---

### Finally, the real deal: full-size, full-color images

Good job once again on decoding the secret fox message!  That means your code is working, and will only need a bit of tweaking
to start applying to full-size, full-color images.

Before we jump into it, can you think of a way to adapt the method for grascale images that we had above 
in order to be able to decode messages from a color image?  Remember, the only difference is that now we have an extra
dimension - which corresponds to an R, G, and B value for each pixel.  Once again, don't worry about how to embed the
message into the image, but just consider what type of scheme might be possible, and how you would decode such a scheme.

As a reminder, we're moving from this:

![gray_sample_image](https://user-images.githubusercontent.com/37650759/155842485-84f976df-ddc6-4a94-870c-4016f7903e25.png)

to this:

![rgb_sample_image](https://user-images.githubusercontent.com/37650759/155842481-ba718d04-e408-46bb-8603-bf97ac7ae87a.png)

---

After a little pondering, hopefully you have some sort of idea for how a message could be decoded from a color image.

---

Here's a really simple idea: remember the concept of `flatten()`-ing an array from before?  Well, we could actually just
flatten our 3D numpy array down to a 1D array, then pretend it was a grayscale image all along and apply exactly the
same algorithm as above to the flattened array.  (Our flattened array will just be three times as long as before.)
If you're curious about the ordering of a flattened 3D numpy array, it goes like this, given a 2x2 RGB image:

`[r_topleft, g_topleft, b_topleft, r_topright, g_topright, b_topright, r_botleft, ...]`

---

But there's something more interesting we could do!  We have three different color channels - Red, Green, and Blue -
what if we wanted to hide three different messages in our image?  We could embed one in each color channel.

In fact, rumor has it that's exactly what's been done to the following image:

![snowflake_hidden_message](https://user-images.githubusercontent.com/37650759/155842867-4fee01f0-88ef-4d58-a260-eaf07e0711c3.png)

They say the length of the message hidden in the red color channel is the sixth prime number. And as for the 
green and blue, surely they have messages too, length unknown...
