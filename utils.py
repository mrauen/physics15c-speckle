from PIL import Image


def scaleImage(filename, scale):
    image = Image.open(filename)
    old_height, old_width = image.size
    image = image.resize((scale * old_height, scale * old_width))
    image.save("%sx_%s" % (scale, filename))
