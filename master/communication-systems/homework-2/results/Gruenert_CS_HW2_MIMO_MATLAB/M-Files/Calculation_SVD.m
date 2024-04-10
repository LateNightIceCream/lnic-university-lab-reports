% script for Calculating EQL-Coefficients 
% of  MIMO-System using SVD

%H=[1 0.3; 0.5 0.8]; % example channel: y1=1*x1+0.3*x2  y2=0.8*x2+0.5*x1
% H   = [0.98   0.15; 0.6 0.8]

H   = [1.0   0.21; 0.39 0.89]

[U S V] = svd(H)   % SV-decomposition
% V = coefficients for precoder
% U'= coefficients for receiver
% S = singular values /relation of eye-openings
Uh=U';

% transfer into the model

% initialisation channel, precoder, postcoder

pre = V;       % precoder
pst = Uh;      % postprocessing


sigma=[S(1,1) S(2,2)];