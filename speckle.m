% Read in the images
image1 = double(imread(''));
image2 = double(imread(''));
image3 = double(imread(''));

% Normalize the intensities to be in (-1, 1)
normalizedimage1 = (image1 ./ 128) - 1;
normalizedimage2 = (image2 ./ 128) - 1;
normalizedimage3 = (image3 ./ 128) - 1;

% Get the array of phases
phaseArray = arrayfun(computePhase, normalizedimage1, normalizedimage2, normalizedimage3);