# TRANSFORMATORGRÖßEN
ratio = 10 / 0.4;

R1 = 0.077;
L1 = 4.52;

R2 = 5.1 * 10^-3;
L2 = 7.25*10^-3;

M  = 180 * 10^-3;

# ESB-GRÖßEN
Mstrich  = M * ratio;

R2strich = R2 * ratio^2;
L2strich = L2 * ratio^2;

X2strich = 2*pi*50 * (L2strich - Mstrich);
XMstrich = 2*pi*50 * Mstrich;

X1strich = 2*pi*50 * (L1 - Mstrich);

#X2strich = 9.74;
Z2strich = R2strich + j * X2strich;
Z1       = R1       + j * X1strich;

U_Zstrich = 10 * 10^3 / sqrt(3); # angle 0

# LASTIMPEDANZ
# (symmetrische Belastung)
Z = 350*10^(-3) + (330 * 10^(-3))*j
#Z = 350*10^(-3)
#Z = j*330*10^(-3)
#Z = 350*10^(-3) - (330 * 10^(-3))*j

#====================================

Zstrich = Z * ratio^2;

I2strich = U_Zstrich / Zstrich;

U_Z2 = I2strich * Z2strich

U_Mstrich = U_Z2 + U_Zstrich

I1 = U_Mstrich / (j * XMstrich) + I2strich # !!

U1 = I1 * Z1 + U_Mstrich

# EINGANGSSPANNUNG
abs_U1 = abs(U1)
deg_U1 = rad2deg(angle(U1))

# LEISTUNGEN
S = 3 * U1  .* conj(I1)
abs_S = abs(S)
deg_S = rad2deg(angle(S))

# VERLUSTLEISTUNG
P_V1   = R1 * abs(I1).^2;
P_V2   = R2strich * abs(I2strich).^2;
P_Vges = 3 .* ( P_V1 + P_V2)
