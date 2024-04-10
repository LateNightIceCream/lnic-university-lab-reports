% Program for calculation of coefficients
% for MIMO-equaliser using zero-forcing principle
% (non-frequency-selective MIMO-channel)

% switch setting pre- or postcoder by "Comment" and "Uncomment"

% H=h; %defined in initial.m?

%H=[1.0 0.3; 0.5 0.8] % channel example: y1=1*x1+0.3*x2  y2=0.5*x1+0.8*x2
%H   = [0.98   0.15; 0.6 0.8]
H   = [1.0   0.21; 0.39 0.89]
% calculation:
eq=inv(H);

% setting precoder:

% pre = eq
% pst = [1   0  ; 0   1  ]

% setting postcoder:

pre = [1   0  ; 0   1  ]
pst = eq


% noise/transmit power enhancement estimation:

% pow_enh = sum(eq'.^2)
% fprintf('Power enhancement factor CH_1 : %3.2f \n',pow_enh(1))
% fprintf('Power enhancement factor CH_2 : %3.2f \n',pow_enh(2))
