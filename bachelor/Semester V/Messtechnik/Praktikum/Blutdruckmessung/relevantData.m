file = csvread("scope_6.csv");

time = file(:,1);
voltage = file(:,2);

offset = mean(voltage(1916 : end))


voltage = voltage(1050:1660);

plot(voltage-offset);