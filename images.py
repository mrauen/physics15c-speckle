#!npython
# flake8: noqa

import math, random

import numpy as np
from PIL import Image


@np.vectorize
def computePhase(pixel1, pixel2, pixel3):
  Asinx = (pixel3 - pixel2) / (3 ** 0.5)
  Acosx = -2 * (pixel3 * 0.5 + pixel2 * 0.5 - pixel1) / 3
  A     = (Asinx ** 2 + Acosx ** 2) ** 0.5

  # Is this the right way to handle this case?
  if A == 0 and Acosx == 0:
    return 0

  guess = math.acos(Acosx / A)
  if math.sin(guess) * Asinx < 0:
    guess = -guess

  return guess % (2 * math.pi)

def saveImage(array, filename):
  PIL_image = Image.fromarray(np.uint8(np.array(array) * 255))
  PIL_image.save(filename)

def getBasePhases(height, width):
  x0 = width / 2
  y0 = height / 2
  basePhases = []
  for y in xrange(height):
    basePhases.append([])
    for x in xrange(width):
      exponent  = -(4 * (x - x0)**2) / (float(width**2))
      exponent += -(4 * (y - y0)**2) / (float(height**2))
      phase     = 2 * math.pi * math.exp(exponent)
      basePhases[y].append(phase % (2 * math.pi))

  # Save image
  saveImage(basePhases, "base_phase.png")

  return basePhases

def getObjectPhases(height, width):
  basePhases = getBasePhases(height, width)
  multiplier = random.uniform(0.5, 10)
  phaseShift = random.uniform(0, 2 * math.pi)

  for row in xrange(height):
    for col in xrange(width):
      basePhases[row][col] = (basePhases[row][col] * multiplier + phaseShift) % (2 * math.pi)
  return basePhases

def makeImages(height, width, numImages = 3, phaseShift = 2 * math.pi / 3, testing = False):
  # Removes randomness from the object of interest for testing
  if testing:
    interest = getBasePhases(height, width)
  else:
    interest = getObjectPhases(height, width)

  reference = getObjectPhases(height, width)
  # Create an empty array with dimensions numImages x height x width
  images = np.empty([numImages, height, width])
  for row in xrange(height):
    for col in xrange(width):
      A = random.uniform(1, 20)
      B = random.uniform(1, 20)
      for image in xrange(numImages):
        interestIntensity  = A * math.cos(interest[row][col] + image * phaseShift)
        referenceIntensity = B * math.cos(reference[row][col])
        images[image][row][col] = interestIntensity + referenceIntensity

  # Save images
  saveImage(images[0], "sample_input_1.png")
  saveImage(images[1], "sample_input_2.png")
  saveImage(images[2], "sample_input_3.png")

  return images

def computePhaseFromThreeImages(images):
  height = len(images[0])
  length = len(images[0][0])
  result = []
  for row in xrange(height):
    result.append([])
    for col in xrange(length):
      result[row].append(computePhase(images[0][row][col], images[1][row][col], images[2][row][col]))
  return result

# Vectorized version of the above (faster iteration over pixels)
def computePhaseFromThreeImagesVec(images):
  return computePhase(images[0], images[1], images[2])

def testComputePhaseWithThreeImages():
  height = 50
  width  = 50
  images = makeImages(height, width, 3, 2 * math.pi / 3, True)
  phases = computePhaseFromThreeImages(images)
  expectedPhases = getBasePhases(height, width)

  for row in xrange(height):
    for col in xrange(width):
      print phases[row][col], expectedPhases[row][col]
      if abs(phases[row][col] - expectedPhases[row][col]) > 0.01:
        raise Exception('Phases not recovered, test failed.')

  return

# Unit test: computePhaseFromThreeImages equivalent to computePhaseFromThreeImagesVec
def testComputePhaseFromThreeImagesVec():
  height = 50
  width  = 50
  images = makeImages(height, width, 3, 2 * math.pi / 3, True)
  phases1 = computePhaseFromThreeImages(images)
  phases2 = computePhaseFromThreeImagesVec(images)

  for row in xrange(height):
    for col in xrange(width):
      if abs(phases1[row][col] - phases2[row][col]) > 0.01:
        raise Exception('Differing phases, test failed')

  return
