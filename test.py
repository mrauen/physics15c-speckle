#!npython

import sys

from math import *
import cPickle as pickle

import numpy as np
import pylab as pl
from scipy import stats


def pick_pixel(x, y):
    cos_values = []
    for image_number in xrange(0, 15):
        image_path = "Burst/%d.png" % image_number
        image = pl.imread(image_path) * 2 - 1
        cos_values.append(image[x][y][1])

    pickle.dump(cos_values, open("cos_values.pickle", "w"))
    plot_pixel()


def plot_pixel():
    cos_values = pickle.load(open("cos_values.pickle", "r"))
    cos_values = np.array(cos_values)

    x = np.arange(0, len(cos_values))
    y = cos_values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    for i in x:
        cos_values[i] = cos_values[i] - (slope * i + intercept)

    pl.plot(x, 5 * cos_values, "o")
    # t = np.arange(0, len(cos_values), 0.1)
    # pl.plot(t, .12 * np.cos(2.0 * t - 1.5))
    pl.axis([0, len(cos_values), -1, 1])
    pl.show()


def main():
    im1 = pl.imread("images/0.png")
    im2 = pl.imread("images/1.png")
    im3 = pl.imread("images/2.png")
    im4 = pl.imread("images/3.png")
    im5 = pl.imread("images/4.png")

    print im1[1000][1000][1], im2[1000][1000][1], im3[1000][1000][1], im4[1000][1000][1], im5[1000][1000][1]

    # phase1 = compute_phase(im1)
    # phase2 = compute_phase(im2)
    # phase3 = compute_phase(im3)


@np.vectorize
def compute_phase(Acosx, value2, value3):
    Asinx = (value3 - value2) / sqrt(3)
    A     = sqrt(Asinx ** 2 + Acosx ** 2)
    cosx  = value1 / A
    sinx  = Asinx / A

    guess = acos(cosx)

    # Verify that the sign of the sine is correct
    if sin(guess) * sinx > 0:
        phase = guess
    else:
        phase = -guess

    return phase

if __name__ == "__main__":
    function = sys.argv[1]
    arguments = sys.argv[2:]
    function_call = "%s(%s)" % (function, ",".join(arguments))
    eval(function_call)
