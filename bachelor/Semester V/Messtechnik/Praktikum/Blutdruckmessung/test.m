file = csvread("scope_6.csv");

time = file(:,1);
voltage = file(:,2);

offset = mean(voltage(1916 : end));

plot(voltage-offset);