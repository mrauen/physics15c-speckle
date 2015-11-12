% Function that computes the underlying cosine function,
% assuming phase shifts of 2*pi/3 and 4*pi/3
function phase = computePhase(Acosx, value2, value3)
    Asinx = (value3 - value2) / sqrt(3);
    A     = sqrt(Asinx^2 + Acosx^2);
    cosx  = Acosx / A;
    sinx  = Asinx / A;

    guess = acos(cosx);
    % Verify that the sign of the sine is correct
    if sin(guess) * sinx > 0
        phase = guess;
    else
        phase = -guess;
    end
end