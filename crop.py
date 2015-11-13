from PIL import Image

w, h = 6016, 4000
count = 0
for image_number in xrange(245, 259 + 1):
    image_name = "Burst/DSC_%04d.JPG" % image_number
    output_name = "Burst/%d.png" % count
    count += 1
    im = Image.open(image_name)
    im.crop((1800, 1200, w - 1500, h)).save(output_name)
