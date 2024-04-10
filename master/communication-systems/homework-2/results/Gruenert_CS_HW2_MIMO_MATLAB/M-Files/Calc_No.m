% Calculation of No for MIMO

% Assumption: - signal power is equally distributed (for this No-calc)
%             - there are independent noise sources per each subchannel 


N = 2; % # subchannels/ direct links
fdata = 20000;
bit_system = 4; % bit per symbol (whole system)
fsym = fdata/bit_system; % necessary symbols per second
Ts = 1/fsym;
Ps =1; % transmit power whole system

Es_No_dB = 19  % given/assumed value

Es_No_lin = 10^(Es_No_dB/10) % relation Es/No

Es = Ps*Ts;

No = Es/(Es_No_lin*N)   % No for all noise sources