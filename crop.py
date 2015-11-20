#!npython

import sys

from PIL import Image


def crop(start, end, folder):
    w, h = 3456, 2592
    count = 0
    for image_number in xrange(start, end + 1):
        image_name = "%s/CIMG%04d.JPG" % (folder, image_number)
        output_name = "%s/%d.png" % (folder, count)
        count += 1
        im = Image.open(image_name)
        im.crop((800, 300, w - 800, h - 500)).save(output_name)
        print image_name

if __name__ == "__main__":
    start, end = sys.argv[1:]
    folder = "consistency_check"
    crop(int(start), int(end), folder)
