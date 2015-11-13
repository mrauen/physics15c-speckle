from PIL import Image
import numpy as np
import pylab as pl


im0 = pl.imread("Burst/0.png")
for image_number in xrange(1, 15):
    # Generate the path. Looks like "Burst/1.png"
    image_path = "Burst/%d.png" % image_number
    # Load the image and subtract off the first one
    image = (pl.imread(image_path) - im0) ** 2 * 10
    # Convert to PIL image
    PIL_image = Image.fromarray(np.uint8(image * 255))
    # Save the resulting image as "Burst/diff_1.png"
    PIL_image.save("Burst/diff_%d.png" % image_number)
