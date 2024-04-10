Un_OS_LL = 10000;
Un_US_LL = 400;

Un_OS_S  = Un_OS_LL / sqrt(3);
Un_US_S  = Un_US_LL / sqrt(3);

Sn = 630 * 10^3;

uk = 0.06;

P0 = 800;
Pk = 6750;

#=================

disp("Aufgabe 1")

In_OS = Sn / (sqrt(3) * Un_OS_LL)
In_US = Sn / (sqrt(3) * Un_US_LL)

In_OS = Sn / (3 * Un_OS_S)
In_US = Sn / (3 * Un_US_S)

Z_T_OS = abs(Un_OS_LL.^2 * uk / Sn)
Z_T_US = abs(Un_US_LL.^2 * uk / Sn)

R_T_OS = 1/3 * Pk / In_OS^2
R_T_US = 1/3 * Pk / In_US^2

X_T_OS = sqrt(Z_T_OS^2 - R_T_OS^2)
X_T_US = sqrt(Z_T_US^2 - R_T_US^2)

Z_T_OS = R_T_OS + j * X_T_OS;

#=================

disp("")
disp("=====")
disp("Aufgabe 2")
disp("a)")

I_L    = In_OS; # vorgabe
cosPhi = 0.7;

I1  = I_L * exp(j * acos(cosPhi) );

U1 = Un_OS_S + I1 * (R_T_OS + j * X_T_OS);

abs(U1)
rad2deg(angle(U1))

disp("=====")
disp("b)")

I_L    = 0.5 * In_OS;
cosPhi = 1;

I1  = I_L * exp(j * acos(cosPhi) );

U1 = Un_OS_S + I1 * (R_T_OS + j * X_T_OS);

abs(U1)
rad2deg(angle(U1))

disp("=====")
disp("c)")

I_L    = 0.8 * In_OS;
cosPhi = 1;

I1  = I_L * exp(j * acos(cosPhi) );

U1 = Un_OS_S - I1 * (R_T_OS + j * X_T_OS);

abs(U1)
rad2deg(angle(U1))


disp("")
disp("=====")
disp("Aufgabe 3")
disp("")

U_ZT_OS_abs = abs(In_OS) * abs(Z_T_OS)

phi_I = rad2deg(pi - acos(U_ZT_OS_abs / (2 * Un_OS_S)) - atan(X_T_OS / R_T_OS))

disp("")
disp("=====")
disp("Kontrolle Aufgabe 3")
disp("")

I_L    = In_OS;
cosPhi = 0.978;

I1  = I_L * exp(j * acos(cosPhi) );

U1 = Un_OS_S - I1 * (R_T_OS + j * X_T_OS);
abs(U1)
