close all
clear all
clc

function result = correlate (x, y)

  if length(x) < length(y)
    error("x must have more vals than y")
  endif
  
  result = zeros(1, length(x));
    
  # pad zeroes to the end
  x_padded = [x, zeros(1, length(y))];
  
  for n = 1:length(x)
  
    for k = 1:length(y)
    
      result(n) += y(k) .* x_padded(n + k);
  
    endfor
  
  endfor

endfunction

Fs = 40;
Ts = 1/Fs;

data = csvread("extraction.csv");

time = data(:, 2)';
voltage = data(:, 3)';
time = time(1:293);
voltage = voltage(1:293);

c = correlate(voltage, voltage);

N  = length(c);

c_spectrum = abs(fft(c))/N;

freq = (0:(N-1)) / (Ts * N); # m / (Ts * N)

[peakVal, peakIndex] = findpeaks(c_spectrum, "MinPeakHeight", 0.0006);
peakFreq = (peakIndex - 1) / (Ts * N);

phase = (arg(fft(c)));


#approximated = c_spectrum(14).*cos(2*pi.*time.*freq(14) + phase(14)) + c_spectrum(1).*sin(2*pi.*time.*freq(1) + phase(1));



hold on
plot(time, voltage)
plot(time, c)
#plot(time, approximated)


#stem(freq, c_spectrum)
#plot(peakFreq, peakVal, "x")
#xlim([0, 20])

hold off

peakFreq(2)



#csvwrite("correlation.csv", [time' c'])
csvwrite("corr_fft.csv", [freq' c_spectrum'])