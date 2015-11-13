% Read in the images
image1 = double(rgb2gray(imread('images/DSC_0115.jpg')));
image2 = double(rgb2gray(imread('images/DSC_0116.jpg')));
image3 = double(rgb2gray(imread('images/DSC_0117.jpg')));

% Normalize the intensities to be in (-1, 1)
normalizedimage1 = (image1 ./ 128) - 1;
normalizedimage2 = (image2 ./ 128) - 1;
normalizedimage3 = (image3 ./ 128) - 1;

% Get the array of phases
phaseArray = arrayfun(@(x, y, z) arrayfun(computePhase, x, y, z), normalizedimage1, normalizedimage2, normalizedimage3);
imshow(phaseArray);