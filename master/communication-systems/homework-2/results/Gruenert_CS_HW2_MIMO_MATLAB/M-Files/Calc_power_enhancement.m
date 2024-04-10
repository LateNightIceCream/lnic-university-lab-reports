% Example for power enhancement calculation 
H  = [0.98 0.2;0.38 0.86]; % example channel
H2 = H.^2             % enhancement of pathes  
Pin  = [0.5;0.5]      % input power  
Pout = H2*Pin         % P_out of layers
Psum=sum(Pout)        % power enhancement by channel

% Noramisation

H_norm=H/sqrt(Psum)