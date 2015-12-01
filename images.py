#!npython
import math, random

def computePhase(pixel1, pixel2, pixel3):
  Asinx = (pixel3 - pixel2) / (3 ** 0.5)
  Acosx = -2 * (pixel3 * 0.5 + pixel2 * 0.5 - pixel1) / 3
  A     = (Asinx ** 2 + Acosx ** 2) ** 0.5

  guess = math.acos(Acosx / A)
  if math.sin(guess) * Asinx < 0:
    guess = -guess

  return guess

def getBasePhases(height, width):
  x0 = width / 2
  y0 = height / 2
  basePhases = []
  for y in xrange(height):
    basePhases.append([])
    for x in xrange(width):
      phase = 2 * math.pi * math.exp(- (x - x0) ** 2 - (y - y0) ** 2)
      basePhases[y].append(phase % (2 * math.pi))
  return basePhases

def getObjectPhases(height, width):
  basePhases = getBasePhases(height, width)
  multiplier = random.uniform(0.5, 10)
  phaseShift = random.uniform(0, 2 * math.pi)

  for row in xrange(height):
    for col in xrange(width):
      basePhases[row][col] = (basePhases[row][col] * multiplier + phaseShift) % (2 * math.pi)
  return basePhases

def makeImages(height, width, numImages = 3, phaseShift = 2 * math.pi / 3):
  # Removes randomness from the object of interest for testing
  testing = False
  if testing:
    interest = getBasePhases(height, width)
  else:
    interest = getObjectPhases(height, width)

  reference = getObjectPhases(height, width)
  A = random.uniform(1, 20)
  B = random.uniform(1, 20)
  images = [[] for _ in xrange(numImages)]
  for image in xrange(numImages):
    for row in xrange(height):
      images[image].append([])
      for col in xrange(width):
        images[image][row].append(A * math.cos(interest[row][col] + image * phaseShift) + B * math.cos(reference[row][col]))
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
