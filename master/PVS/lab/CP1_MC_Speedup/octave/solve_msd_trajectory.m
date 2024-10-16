function [tout, xout] = solve_msd_trajectory(mass_m, spring_k, damper_d, t_bounds, initial_force)

  % starting values
  % x0 = 0
  % x'0 = 0
  x = [0 0]';

  % step size
  h = 0.05;

  tout = [];
  xout = [];

  for t = t_bounds(1):h:t_bounds(2)

    tout = [tout t];
    xout = [xout; x'];

    xdot = msd_dot(t, x, mass_m, spring_k, damper_d, initial_force);

    x(1) = x(1) + h * xdot(1);
    x(2) = x(2) + h * xdot(2);
  endfor

end
