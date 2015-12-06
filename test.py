#!npython

from math import *
import cPickle as pickle
from PIL import Image

import numpy as np
import pylab as pl
#from scipy import stats

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


def computePhaseFirstThree(folder):
    import math
    #transformation = np.vectorize(math.sqrt)
    #transformation = np.vectorize(lambda x: x ** 2)
    transformation = np.vectorize(lambda x: x)  # identity
    im1 = transformation(rgb2gray(pl.imread("%s/0.png" % folder)))
    im2 = transformation(rgb2gray(pl.imread("%s/1.png" % folder)))
    im3 = transformation(rgb2gray(pl.imread("%s/2.png" % folder)))

    result = images.computePhase(im1, im2, im3)
    pickle.dump(result, open("%s.pickle" % folder, "w"))


def show_phase(folder):
    result = pickle.load(open("%s.pickle" % folder, "r"))
    image = result / (2 * pi) + 0.5
    img = Image.fromarray(np.uint8(image * 255))
    img.save("%s.png" % folder)


def diff_images(input1, input2, output):
    im1 = pl.imread(input1)
    im2 = pl.imread(input2)
    diff = (im1 - im2 + 1) % 1
    for _ in xrange(5):
        newDiff = []
        for row in xrange(len(diff)):
            newDiff.append([])
            for col in xrange(len(diff[row])):
                adjacentPixels = [(row - 1, col - 1), (row, col - 1), (row - 1, col), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1), (row, col + 1), (row + 1, col)]
                adjacentPixels = [(r, c) for (r, c) in adjacentPixels if r >= 0 and r < len(diff) and c >= 0 and c < len(diff[row])]
                adjacentValues = [diff[r][c] for (r, c) in adjacentPixels]
                newDiff[row].append(sum(adjacentValues) / len(adjacentValues))
        diff = newDiff
    img = Image.fromarray(np.uint8(diff * 255))
    img.save(output)

computePhaseFirstThree('reference')
computePhaseFirstThree('shifted')
show_phase('reference')
show_phase('shifted')
diff_images('reference.png', 'shifted.png', 'output.png')
