% initialising baseband simulation Matlab/Simulink R2021a

disp('M12 2x2 MIMO-Transmission: Zero-Forcing Equaliser and SVD');

% setting search path

path_alt = matlabpath;
cf = pwd;
cf1= [cf,';'];
if ispc  
   mp = [cf,'\Models;'];
   mp1= [cf,'\Models\'];
   mf = [cf,'\M-Files;'];
end
if isunix  
   mp = [cf,'/Models;'];
   mp1= [cf,'/Models/'];
   mf = [cf,'/M-Files;'];
end

p = [cf1,mp,mf];
path(p, path_alt);

cd(mp1);

clear

close_system ('GeneralASKLib',0)
close_system ('NoiseLib_2021',0)

% setting parameters for simulation
% baseband

Tbit5_0 = 1/5000;     %5.0 kBit
Tbit2_5 = 1/2500;     %2.5 kBit
Tsk = 1/80000;        % 5kbit/s and 16pts/symbol  

%% ASK-system parameters:
%------------------------------------------------------------
M1=8;               % Initialisation # of steps/ bitload
M2=2;
B1=log2(M1);        % bitload
B2=log2(M2);

%pl1=1;              % powerloading factors
%pl2=1;

L=2;
sigM1_g = ASKpunkte_gray(M1);   % constellation L1
sigM2_g = ASKpunkte_gray(M2);   % constellation L2

% BER-delays flexible
delay1=B1*11;
delay2=B2*11;
if delay1==11
    delay1=9;
end
if delay2==11
    delay2=9;
end

       
%sigma=[1.0 1.0];           % singular values   


% % ASK-signal constellation
% M=2;                        % Initialisation # of steps
% sig2up =[0 1];              % signal constellation 2-ASK unipolar
% sig2bp =[-1 1];             % signal constellation 2-ASK bipolar
% sig4   =ASKpunkte(4);       % signal constellation 4-ASK
% sig4gr =[sig4(1) sig4(2) sig4(4) sig4(3)]; % gray-coded
% sig16  =ASKpunkte(16);      % signal constellation 16-ASK
% 
% % BER- initial parameter/ adjustment inside model 
% nAuge  = 13;                
% nsteps = 1210;              
% nAuge2 = 12;                    
% nsteps2= 608;                
% sigdem = sig4;               
% sigdem2 =sig2bp;              
% sigdem2up =sig2up;  
% 
% constellation = sig2bp;
% const_dem = sigdem2;

% initialisation channel, precoder, postcoder

H = [1.0 0.21; 0.39 0.89];

[U,S,V] = svd(H)

%pre = [1   0  ; 0   1  ];  
pre = V;


%pst = [1   0  ; 0   1  ];
%pst = inv(H); % ZF
pst = U';

%sigma=[1 1];
sigma=[S(1,1) S(2,2)];


Ps1=0.55;    
Ps2=0.45;

sigma1      = S(1,1)           % scaling L1 by svd ( S(1,1) )
sigma2      = S(2,2)  

Us1=sqrt(Ps1/((M1^2-1)/3))
Us2=sqrt(Ps2/((M2^2-1)/3))

g1=sqrt(2/(((sigma1*Us1)/(sigma2*Us2))^2+1)); % calc gain/att. for L1
g2=sqrt(2-g1^2);

pl=[g1^2 g2^2];  % creation of vector representation of powerfactors
p_abs=pl*0.5;   % absolute power value on layers

t1=g1*sigma1;   % test g1 sigma1 = g2*sigma2
t2=g2*sigma2;

pl1=pl(1);
pl2=pl(2);

% open models
M12_addBlox
M12_MIMO_flexBitLoad

