% CP1/MC
% 0. ode45 in m-code als Referenzlösung
% 1. in m-code mit Euler-Verfahren
% 2. in m-code mit Rust sequentiell
% 3. in m-code mit Rust parallel

close all;
clc;

% system model parameters
mass   = 0.1;
spring = 1.0;

% this should be varied
damper = 0.6;

damper_bounds = [800 1200];

t_bounds = [0 2]

init_force = 5;

% m * s''(t) + d * s'(t) + s * s(t) = 0
% s''(t) = - 1/m * (d * s'(t) + s * s(t))
% subst
% x1(t) = s(t)
% x2(t) = s'(t)
%   => 1.: x1'(t) = x2(t)
%   => 2.: x2'(t) = -1/m * (d * x2(t) + s * x1(t))

[toutb, xout] = solve_msd_trajectory(mass, spring, damper, t_bounds, init_force);

%size(xout)

b = xout(:,2);
%plot(tout, a)



global mass spring damper init_force

% system model parameters
mass   = 0.1;
spring = 1.0;

% this should be varied
damper = 0.6;

init_force = 5;

% m * s''(t) + d * s'(t) + s * s(t) = 0
% s''(t) = - 1/m * (d * s'(t) + s * s(t))
% subst
% x1(t) = s(t)
% x2(t) = s'(t)
%   => 1.: x1'(t) = x2(t)
%   => 2.: x2'(t) = -1/m * (d * x2(t) + s * x1(t))

% initial values
x = [0 0]';

t = 0;
tfinal = 2.0;


[tout, xout] = ode45('msd_dot_ode45', [t tfinal], x);

a = xout(:,2);


plot(tout, a, 'x', toutb, b, 'o-')
