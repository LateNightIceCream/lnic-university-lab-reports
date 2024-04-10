% Powerfactor calculation including bitload
% according idea of same quality

Ps1=0.5;    % w/o powerloading
Ps2=0.5;


% example result of SVD:
sigma1      = S(1,1)           % scaling L1 by svd ( S(1,1) )
sigma2      = S(2,2)           % scaling L2 by svd ( S(2,2) )

% bitloads
bit1=2   % bitload
bit2=2
M1=2^bit1   % modulation grade (number of symbols in const.)
M2=2^bit2
M1=4
M2=4
Us1=sqrt(Ps1/((M1^2-1)/3))
Us2=sqrt(Ps2/((M2^2-1)/3))

%------------------------------------------------------------------
% idea: same quality = same Ua (this formula pays no respect to the 
% higher importance of layer with probably more bitload!!)
%------------------------------------------------------------------

g1=sqrt(2/(((sigma1*Us1)/(sigma2*Us2))^2+1)) % calc gain/att. for L1
g2=sqrt(2-g1^2)                              % g1^2+g2^2=2   

pl=[g1^2 g2^2]  % creation of vector representation of powerfactors
p_abs=pl*0.5    % absolute power value on layers

t1=g1*sigma1   % test g1 sigma1 = g2*sigma 2
t2=g2*sigma2