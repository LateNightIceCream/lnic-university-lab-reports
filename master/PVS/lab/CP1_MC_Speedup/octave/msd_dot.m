function ydot = msd_dot(t, y, m, s, d, f0)
  % input: array of states (x1, x2) [(position) (derivative of position)]
  % output: array of derivative of states (x1', x2') [(derivative of position) (derivative of derivative of position)]

  ydot = [
    y(2);
    1/m * (f0 - d * y(2) - s * y(1))
  ];

end
