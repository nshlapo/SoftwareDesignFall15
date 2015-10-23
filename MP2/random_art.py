from random import randint
from PIL import Image
from math import sin, cos, pi

def build_random_function(min_depth, max_depth):
    """ Creates a nested list of strings that represents a randomly generated
        function.

        Recurses a random number of times between min_depth and max_depth.
    """
    depth = randint(min_depth, max_depth)

    def rand_func(rec):
        """ The recursive function which continues to be called until rec is 0.
            Each call of this function reduces rec by 1.
        """

        # maximum recursion has been reached, begin passing up the outputs
        if rec is 0:
            var = ['x', 'y']
            rand = randint(0,1)
            return var[rand]

        # randomly decide what function to return, then recursively return the
        # number of inputs it needs
        rand = randint(0,2)
        if rand is 0:
            return ['sin_pi', rand_func(rec - 1)]
        elif rand is 1:
            return ['prod', rand_func(rec - 1), rand_func(rec - 1)]
        elif rand is 2:
            return ['cos_pi', rand_func(rec - 1)]

    # start the recursion call
    # interested use of the nested functions to work with min/max depth!
    f = rand_func(depth)
    return f


def evaluate_random_function(f, x, y):
    """ Takes in a randomly generate function in the form of nested lists of
        strings, x and y, and then return value of function at that point and
        time.

        f: the randomly generated function
        x, y: coordinates of pixel in generated frame
    """
    def translate(list1):
        """ Recursive function returns nested list as mathematical expression
        """
        # these cases end the recursion
        if list1 is 'x':
            return x
        elif list1 is 'y':
            return y
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

def create_image(px, py, min_depth, max_depth, filename):
    """ Creates one frame of video based on 3 random functions, frame size,
        and desired depths.

        px, py: the size of the frame in pixels
        min_depth, max_depth: depth inputs to build_random_function
        filename: name to save image to
        t: frame of video
        red, green, blue: unique random function for each pixel value
    """

    # unique random functions for each RGB value that are generated for each image
    red = build_random_function(min_depth, max_depth)
    green = build_random_function(min_depth, max_depth)
    blue = build_random_function(min_depth, max_depth)

    z = []
    # iterate over each pixel
    for i in range(px):
        for j in range(py):
            map_i = remap_interval(i, 0, px-1, -1, 1)
            map_j = remap_interval(j, 0, py-1, -1, 1)

            rval = evaluate_random_function(red, map_i, map_j)
            gval = evaluate_random_function(green, map_i, map_j)
            bval = evaluate_random_function(blue, map_i, map_j)

            r = int(remap_interval(rval, -1, 1, 0, 255))
            g = int(remap_interval(gval, -1, 1, 0, 255))
            b = int(remap_interval(bval, -1, 1, 0, 255))
            # create a list of tuples to represent pixel RGB values
            z.append((r,g,b))
    # use pixel list to create a .png file
    im = Image.new("RGB",(px,py))
    im.putdata(z)
    im.save(filename, 'PNG')

if __name__ == '__main__':
    # create 20 random images of given depth and size
    for i in range(20):
        create_image(350, 350, 10, 'example' + str(i) + '.png')