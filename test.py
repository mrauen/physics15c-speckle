#!npython

from math import *
import cPickle as pickle
from PIL import Image

import numpy as np
import pylab as pl
from scipy import stats

import images


def pick_pixel(x, y):
    cos_values = []
    for image_number in xrange(0, 5):
        image_path = "consistency_check/%d.png" % image_number
        image = pl.imread(image_path) * 2 - 1
        cos_values.append(image[x][y][1])
        print image_path

    pickle.dump(cos_values, open("cos_values.pickle", "w"))
    print cos_values
    plot_pixel()


def plot_pixel():
    cos_values = pickle.load(open("cos_values.pickle", "r"))
    cos_values = np.array(cos_values)

    x = np.arange(0, len(cos_values))
    # y = cos_values
    # slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    # for i in x:
    #     cos_values[i] = cos_values[i] - (slope * i + intercept)

    pl.plot(x, cos_values, "o")
    # t = np.arange(0, len(cos_values), 0.1)
    # pl.plot(t, .12 * np.cos(2.0 * t - 1.5))
    pl.axis([0, len(cos_values), -1, 1])
    pl.show()


def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def main():
    import math
    transformation = np.vectorize(math.sqrt)
    #transformation = np.vectorize(lambda x: x ** 2)
    im1 = transformation(rgb2gray(pl.imread("cosine_check/0.png"))) * 2 - 1
    im2 = transformation(rgb2gray(pl.imread("cosine_check/1.png"))) * 2 - 1
    im3 = transformation(rgb2gray(pl.imread("cosine_check/2.png"))) * 2 - 1

    result = images.computePhase(im1, im2, im3)
    pickle.dump(result, open("phase.pickle", "w"))


def show_phase():
    result = pickle.load(open("phase.pickle", "r"))
    image = result / (2 * 3.1416) + 0.5
    img = Image.fromarray(np.uint8(image * 255))
    img.save("output.png")
