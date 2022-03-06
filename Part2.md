## Encoding Your Own Messages

### Hello again ;)

Welcome to Part Two, in which you will encode your own secret messages in an image of your choice!

---

You were probably wondering, so how did I encode those messages in the images in the first place?
And how did I do it so the images look so normal?  Well, let's start with the first question.

First we need to recall how the messages were decoded.  Let's just consider one channel for now,
for simplicity, since they're all independent.  So we take all the pixel values from the red channel,
group them into `message_length` groups (e.g. 13 groups for a message of length 13), and then compute
the sum within each group.  Finally, we do some math to convert that sum into an index into our alphabet,
and that gives us a character.  Concatenating these characters together gives us the message.

Now we want to do the opposite of this.  First, we convert our characters into indices: this represents
the modular sums that we would hope to obtain for our pixel groups.  Let's call these our `target_sums`.
Next, we go through and compute the **actual sums**, and we'll probably get some different values
(unless we're insanely lucky!).  So maybe something like this (recalling our example of just a grayscale
image for now, with a message length of 3):

![encoding_target_sums_diagram](https://user-images.githubusercontent.com/37650759/156912482-cf33994c-1fec-4c9f-aac9-83bb525527e7.png)

Given that you know how far off each group sum is from the target, what's an easy way to modify the image
so that the sums equal the targets?

Think about this for a minute and see if you have an idea.

---

<details>
  <summary>Initial Solution</summary>
  
  You might have thought of something more interesting, but here's the most basic, unimaginative solution:
  Select the first `message_length` pixels of the image to act as the representatives for each group.  Modify
  their values by the corresponding difference between target and actual solution for that group.
  
  So in the first group, the target was 1 less than the actual sum.  Thus we subtract 1 from the pixel at index 0.
  Next, we had a target 23 greater than the actual sum, so we add 23 to the pixel at index 1.  And so on...
</details>

The initial solution described above is very naive.  What sort of problems can you spot with it?

---

### Refining the Solution

What would happen, for instance, if a pixel was black in our image (so its value is zero), but the target
sum was higher than the actual sum?  How would you refine your approach (maybe you already did) to handle
this situation?

<details>
  <summary>Refined Solution</summary>
  
  There are two very natural approaches here:
  
  One approach is that rather than simply using the first pixel from each group as our representative, we can iterate through
  all the pixels within a given group (which equates to incrementing our index by `message_length` at each step)
  until we find a pixel that can be incremented or decremented by the amount required, while staying in the range [0, 255].
  
  Another approach is to remember that everything we are doing here is modular arithmetic - that means the numbers operate
  in a cycle.  Think of the second group in our example above: the target sum was 25 and the actual sum was 2.  If our
  alphabet length is 27, that means 27 = 0, 28 = 1, 29 = 2, and so on.  So in fact, rather than saying our target sum was 23 too high,
  we could say it was `25 - 29 = -4` off, or 4 too low.  This means we always have two options: we could either add some amount,
  or subtract some amount.  And as long as the alphabet isn't super long, one of these will always be possible!
  
</details>

---

### Embedding Your First Message

There are of course some more concerns, like that assumption we mentioned above ("as long as the alphabet isn't super long"),
but you've got a solution that works, and you can now embed your own message in an image!

Let's start with a small image and a short message for easy debugging, like we did with the decoding case.
Pick a 3-4 character message you want to embed in an image!

Next, create a random grayscale image to start yourself off with.  You can use this function to generate a random
but consistent image for testing:

```python
def GenerateRandomGrayscaleImage(num_rows: int, num_cols: int) -> np.ndarray:
    # Set the RNG seed for consistent results, so debugging is easier
    # Change the seed or comment out this line as desired
    np.random.seed(0)
    flat_array = np.random.randint(0, 256, num_rows * num_cols)
    return flat_array.reshape(num_rows, num_cols)
```

You can now treat this as your input image array.  See if you can adjust the image pixels so that it
contains the secret message you chose.  And if you had a different, more interesting solution that the one(s)
I outlined above, use yours!

Once you've updated the image matrix to contain the modified pixel values, save the image using the `SaveImage` function
from the previous part.  One trick though: if your numpy array's data type is not `uint8` when you save the image,
the image library will assume that you're using a different value scale than 0-255, and so the image won't look right.
You can convert it to the `uint8` data type like this:

```python
my_image_array = ...  # numpy array to convert
final_image_array = my_image_array.astype('uint8')
SaveImage(final_image_array, 'output_filename.png')
```

Now a question for you: how can you test and see if you embedded the message correctly in your image?

(Hint: this should take almost no work, you already have the code needed to do this!)

Once you've tested this part and seen that the message you decode from this image matches the message
you wanted to encode, we can move on to the most fun part!  By the way, make sure you're testing fully
end-to-end, which means loading the image from the file you saved it to, then decoding the message
from that loaded numpy array (rather than just encoding to a numpy array and decoding from that directly)
so that you ensure all parts of your algorithm are working correctly!  It's going to get much harder to debug
once we move on to full size color images.

---

### Full Size Image & Messages, Yay!

This next part should be the most fun: Go pick an image that you want to embed your message into!

Next, pick your secret messages: one for each color channel.  And while you're at it, select your own "alphabet" (this is the cryptography
term for what you've called `CHAR_ARRAY` in your code).  Maybe add some more punctuation or other symbols,
lowercase, uppercase, numbers, whatever you want to spice up your message!

Now it's time to encode the messages!  Adapt your previous code to be able to handle the three channels in 
a color image, and make sure you've made any changes you need to account for your new alphabet
(ideally, the only change you needed to make was just the change to your alphabet constant at the top).

Now, can you use your decoding code to verify everything is working?  If it is, send me your image!
I'll try to see if I can decode the message.  I'll just need you to also tell me the alphabet you used :)

---

### Create Your Own Message Encoding Scheme

So all this time, we've been working with this encoding system that I forced upon you and made you use.
But I'm sure at some point you must've wondered how you would embed messages in your own way.  I want you
to go back to that question now, maybe with a whiteboard or a pen and paper, and start outlining the thoughts
that come to you.  Remember that an image is just an array of numbers, so this is your starting point.
What you're designing is just a conversion of some form between a big array of numbers, and a relatively
shorter sequence of characters.
Also, decoding the message tends to be easier than encoding, so you probably want to start by considering the decoding process.

Once you've got a rough idea, take a picture of any diagrams or notes you've made and send it to me.  Let's
talk it over, iron out the details, and see if it's something that could actually be implemented!  Also, if you 
had a cool idea for the decoding process, but were getting stuck on how to encode, this would be a great time
to see if we can solve that together.
