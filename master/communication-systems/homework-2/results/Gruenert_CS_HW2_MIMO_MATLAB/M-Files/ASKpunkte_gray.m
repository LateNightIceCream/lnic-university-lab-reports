function [ sig ] = ASKpunkte_gray( M )
%ASKpunkte( M ) bestimmt aus der Anzahl der Symbolpunkte
%die Lage im reellen Signalraum. Ziel:Ps=1V*V

Us = sqrt(1/((M^2-1)/3));
n = M/2;
signeg = [];
sigpos = [];
faktor= 1:2:M-1;
sigpos = Us*faktor;
signeg = -(fliplr(sigpos));

siglin  = [signeg sigpos];
linpos  = (0:M-1);                      % vector 0...M
newpos  = gray2bin(linpos,'pam',M);     % Gray-order
sig     = siglin(newpos+1);             % sig-level in Gray-order



end

