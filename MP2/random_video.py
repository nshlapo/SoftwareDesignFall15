from random import randint
from PIL import Image
from math import sin, cos, pi
from os import system

def build_random_function(min_depth, max_depth):
    """ Creates a nested list of strings that represents a randomly generated
        function.

        Recurses a random number of times between min_depth and max_depth
    """
    depth = randint(min_depth, max_depth)

    def rand_func(rec):
        """ The recursive function which continues to be called until rec is 0.
            Each call of this function reduces rec by 1.
        """

        # maximum recursion has been reached, begin passing up the outputs
        if rec is 0:
            var = ['x', 'y', 't', 'x', 'y']
            # alter the ratios of x, y, and t
            rand = randint(0, 5)
            return var[rand]

        rand = randint(0,3)
        # randomly decide what function to return, then recursively return the
        # number of inputs it needs
        if rand is 0:
            return ['sin_pi', rand_func(rec-1)]
        elif rand is 1:
            return ['prod', rand_func(rec-1), rand_func(rec-1)]
        elif rand is 2:
            return ['cos_pi', rand_func(rec-1)]
        elif rand is 3:
            return ['sum', rand_func(rec-1), rand_func(rec-1)]

    # start the recursion call
    f = rand_func(depth)
    return f


def evaluate_random_function(f, x, y, t):
    """ Takes in a randomly generate function in the form of nested lists of
        strings, x, y and t, and then return value of function at that point and
        time.

        f: the randomly generated function
        x, y: coordinates of pixel in generated frame
        t: the frame number of the video
    """
    def translate(list1):
        """ Recursive function returns nested list as mathematical expression
        """

        # these cases end the recursion
        if list1 is 'x':
            return x
        elif list1 is 'y':
            return y
        elif list1 is 't':
            return t
        # these cases continue the recursion
        elif list1[0] is 'sin_pi':
            sine = sin(pi*translate(list1[1]))
            return sine
        elif list1[0] is 'cos_pi':
            cosine = cos(pi*translate(list1[1]))
            return cosine
        elif list1[0] is 'prod':
            product = translate(list1[1])*translate(list1[2])
            return product
        elif list1[0] is 'sum':
            suma = translate(list1[1])+translate(list1[2])
            return suma

    # start the recursive call
    z = translate(f)
    return z

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).

        val: value in input range to be remapped
        input_interval_start: start of input range
        input_interval_end: end of input range
        output_interval_start: start of output range
        output_interval_end: end of output range
    """

    in_len = input_interval_end - input_interval_start
    out_len = output_interval_end - output_interval_start
    in_ratio = (input_interval_end - val) / float(in_len)
    out = output_interval_end - in_ratio*out_len

    return out

# this looks good but don't forget you can import your functions from
# your other code - no need to copy-paste

def create_image(px, py, min_depth, max_depth, filename, t, red, green, blue):
    """ Creates one frame of video based on 3 random functions, the frame number,
        frame size, and desired depths

        px, py: the size of the frame in pixels
        min_depth, max_depth: depth inputs to build_random_function
        filename: name to save image to
        t: frame of video
        red, green, blue: consistent unique random function for each pixel value
    """

    z = []
    # iterate over each pixel
    for i in range(px):
        for j in range(py):
            map_i = remap_interval(i, 0, px-1, -1, 1)
            map_j = remap_interval(j, 0, py-1, -1, 1)
            map_t = remap_interval(t, 0, 75, -1, 1)

            rval = evaluate_random_function(red, map_i, map_j, map_t)
            gval = evaluate_random_function(green, map_i, map_j, map_t)
            bval = evaluate_random_function(blue, map_i, map_j, map_t)

            r = int(remap_interval(rval, -1, 1, 0, 255))
            g = int(remap_interval(gval, -1, 1, 0, 255))
            b = int(remap_interval(bval, -1, 1, 0, 255))
            # create a list of tuples to represent pixel RGB values
            z.append((r,g,b))
    # use pixel list to create .png file
    im = Image.new("RGB",(px,py))
    im.putdata(z)
    im.save('temp/' + filename , 'PNG')

if __name__ == '__main__':
    #use consistent generated functions for each frame
    red = build_random_function(0,8)
    green = build_random_function(2,5)
    blue = build_random_function(1,7)

    # generate all frames of video
    for t in range(75):
        # need to give each frame a unique name that will be ordered appropriately
        print 'Generating frame ' + str(t)
        create_image(350, 350, 2, 10, str(t+10) + '.png', t, red, green, blue)

    #system calls to use ffmpeg to create video of images and then remove temporary images and folder
    system("mkdir temp")
    system("ffmpeg -framerate 15 -pattern_type glob -i './temp/*.png' -vb 20M ./mov5.avi")
    system("rm -r ./temp")