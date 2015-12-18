from random import randint
from PIL import Image
from math import sin, cos, pi
from os import system
from random_art import evaluate_random_function, remap_interval, build_random_function, create_image

if __name__ == '__main__':
    #use consistent generated functions for each frame
    red = build_random_function(0,8,4)
    green = build_random_function(2,5,4)
    blue = build_random_function(1,7,4)

    # generate all frames of video
    for t in range(75):
        # need to give each frame a unique name that will be ordered appropriately
        print 'Generating frame ' + str(t)
        create_image(350, 350, 2, 10, str(t+10) + '.png', t, red, green, blue)

    #system calls to use ffmpeg to create video of images and then remove temporary images and folder
    system("mkdir temp")
    system("ffmpeg -framerate 15 -pattern_type glob -i './temp/*.png' -vb 20M ./mov5.avi")
    system("rm -r ./temp")