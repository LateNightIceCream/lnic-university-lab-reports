function ydot = msd_dot(t, y, m, s, d, f0)

  global mass spring damper init_force


  ydot = [
    y(2);
    1/mass * (init_force - damper * y(2) - spring * y(1))
  ];

end
